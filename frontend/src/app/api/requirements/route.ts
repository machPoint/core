import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const limit = searchParams.get('limit') || '50';
    const offset = searchParams.get('offset') || '0';
    const search = searchParams.get('search') || '';
    const category = searchParams.get('category') || '';
    
    // Check if FDS is running
    let healthCheck;
    const fdsUrls = ['http://127.0.0.1:8001', 'http://localhost:8001'];
    let lastError = null;
    
    for (const fdsUrl of fdsUrls) {
      try {
        console.log(`Trying FDS at: ${fdsUrl}`);
        healthCheck = await fetch(`${fdsUrl}/health`, { 
          method: 'GET',
          headers: { 'Accept': 'application/json' },
          signal: AbortSignal.timeout(5000) // 5 second timeout
        });
      
        if (!healthCheck.ok) {
          throw new Error(`Health check failed with status: ${healthCheck.status}`);
        }
        
        const healthData = await healthCheck.json();
        console.log(`FDS Health Check successful at ${fdsUrl}:`, healthData);
        break; // Successfully connected, exit loop
        
      } catch (error) {
        console.error(`FDS Health Check Error for ${fdsUrl}:`, error);
        lastError = error;
        healthCheck = null;
      }
    }
    
    // If no URL worked, return error
    if (!healthCheck) {
      return NextResponse.json({
        error: 'Data engine is not running',
        message: `Cannot connect to data engine: ${lastError instanceof Error ? lastError.message : 'All connection attempts failed'}`,
        requirements: [],
        total: 0
      }, { status: 503 });
    }

    // Determine which FDS URL worked from health check
    const fdsBaseUrl = healthCheck.url.replace('/health', '');
    console.log(`Using FDS base URL: ${fdsBaseUrl}`);
    
    // Build query parameters for FDS backend
    const params = new URLSearchParams({
      limit: limit,
    });
    
    // Note: FDS backend doesn't support offset/search yet, but supports filtering
    if (category) params.append('category', category);

    // Fetch from the FDS admin API which has access to database requirements
    const response = await fetch(`${fdsBaseUrl}/mock/admin/requirements?${params.toString()}`);
    
    if (!response.ok) {
      throw new Error(`FDS responded with status: ${response.status}`);
    }

    const data = await response.json();
    
    // Apply search filter on frontend if needed (since backend may not support it yet)
    let filteredRequirements = data.requirements || [];
    
    if (search) {
      const searchLower = search.toLowerCase();
      filteredRequirements = filteredRequirements.filter((req: any) => 
        req.title?.toLowerCase().includes(searchLower) ||
        req.text?.toLowerCase().includes(searchLower) ||
        req.requirement_id?.toLowerCase().includes(searchLower)
      );
    }
    
    // Apply pagination on frontend
    const startIndex = parseInt(offset);
    const endIndex = startIndex + parseInt(limit);
    const paginatedRequirements = filteredRequirements.slice(startIndex, endIndex);
    
    // Transform the data to match the frontend interface
    const requirements = paginatedRequirements.map((req: any) => ({
      id: req.id || req.requirement_id,
      title: req.title || req.requirement_id,
      type: "requirement" as const,
      status: req.status === "active" ? "active" : 
              req.status === "completed" ? "completed" : "pending",
      lastUpdated: req.extracted_at ? new Date(req.extracted_at).toLocaleString() : "Unknown",
      owner: req.metadata?.owner || "System",
      tags: req.tags || [req.category || "goes-r"].filter(Boolean),
      category: req.category || "system",
      priority: req.priority || "medium",
      verification_method: req.verification_method,
      text: req.text,
      source_document: req.document_id,
      source_page: req.source_page,
      confidence: req.extraction_confidence
    })) || [];

    return NextResponse.json({
      success: true,
      requirements,
      total: filteredRequirements.length,
      pagination: {
        limit: parseInt(limit),
        offset: parseInt(offset),
        hasMore: (parseInt(offset) + requirements.length) < filteredRequirements.length
      }
    });

  } catch (error) {
    console.error('Error fetching requirements:', error);
    
    return NextResponse.json({
      error: 'Failed to fetch requirements',
      message: error instanceof Error ? error.message : 'Unknown error occurred',
      requirements: [],
      total: 0
    }, { status: 500 });
  }
}