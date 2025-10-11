import { NextRequest, NextResponse } from 'next/server';

// Types matching the AIChatPanel component
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
}

interface ChatRequest {
  message: string;
  history: ChatMessage[];
  context_type?: string;
  context_id?: string;
  include_requirements?: boolean;
  requirement_filters?: {
    status?: string;
    category?: string;
    criticality?: string;
  };
}

export async function POST(request: NextRequest) {
  try {
    const body: ChatRequest = await request.json();
    
    // Get OpenAI API key from environment
    const openaiApiKey = process.env.OPENAI_API_KEY || process.env.VITE_OPENAI_API_KEY;
    
    if (!openaiApiKey) {
      return NextResponse.json(
        { error: 'OpenAI API key not configured' },
        { status: 500 }
      );
    }

    // Prepare the messages for OpenAI
    const systemMessage = `You are an AI assistant helping with CORE-SE requirements traceability system. 
    You can help with requirements analysis, database queries, and system insights.`;
    
    // Build context information
    let contextInfo = '';
    switch (body.context_type) {
      case 'requirement':
        if (body.context_id) {
          contextInfo += `Currently viewing requirement: ${body.context_id}. `;
        }
        break;
      case 'jira':
        if (body.context_id) {
          contextInfo += `User is working with Jira ticket ${body.context_id}. `;
        }
        contextInfo += `You can help with issue analysis, sprint planning, and project tracking. `;
        break;
      case 'jama':
        if (body.context_id) {
          contextInfo += `User is working with Jama requirement ${body.context_id}. `;
        }
        contextInfo += `You can help with requirements analysis, traceability, and compliance. `;
        break;
      case 'email':
        if (body.context_id) {
          contextInfo += `User is working with email thread ${body.context_id}. `;
        }
        contextInfo += `You can help with composing, analyzing, and organizing email communications. `;
        break;
      case 'outlook':
        if (body.context_id) {
          contextInfo += `User is working with Outlook meeting/item ${body.context_id}. `;
        }
        contextInfo += `You can help with calendar management, email organization, and scheduling. `;
        break;
      case 'windchill':
        if (body.context_id) {
          contextInfo += `User is working with Windchill part/drawing ${body.context_id}. `;
        }
        contextInfo += `You can help with product lifecycle management, CAD data, and engineering processes. `;
        break;
      case 'database':
        if (body.context_id) {
          contextInfo += `User is working with database record ${body.context_id}. `;
        }
        contextInfo += `You can help with queries and data analysis. `;
        break;
      default:
        contextInfo += `User is working with general CORE-SE requirements traceability system. `;
    }
    
    if (body.include_requirements) {
      contextInfo += `User has access to requirements database with filtering options. `;
    }

    const messages = [
      {
        role: 'system',
        content: systemMessage + contextInfo
      },
      // Include recent history (last 10 messages to avoid token limits)
      ...body.history.slice(-10).map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      {
        role: 'user',
        content: body.message
      }
    ];

    // Make request to OpenAI
    const openaiResponse = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${openaiApiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: process.env.MODEL || 'gpt-4o',
        messages: messages,
        temperature: 0.7,
        max_tokens: 1000
      })
    });

    if (!openaiResponse.ok) {
      const error = await openaiResponse.text();
      console.error('OpenAI API error:', error);
      return NextResponse.json(
        { error: 'Failed to get AI response' },
        { status: 500 }
      );
    }

    const openaiData = await openaiResponse.json();
    const aiMessage = openaiData.choices[0]?.message?.content || 'Sorry, I could not generate a response.';

    // Generate suggestions based on context
    let suggestions: string[] = [];
    switch (body.context_type) {
      case 'requirement':
        suggestions = [
          'Analyze impact of this requirement',
          'Show related requirements',
          'Generate test cases for this requirement',
          'Check compliance status'
        ];
        break;
      case 'jira':
        suggestions = [
          'Analyze sprint velocity and trends',
          'Create user stories from requirements',
          'Generate test cases for this issue',
          'Review issue dependencies'
        ];
        break;
      case 'jama':
        suggestions = [
          'Check requirements traceability',
          'Validate requirement completeness',
          'Generate compliance report',
          'Analyze requirement coverage'
        ];
        break;
      case 'email':
        suggestions = [
          'Draft project status email',
          'Summarize meeting notes',
          'Create action items from discussion',
          'Compose requirement clarification'
        ];
        break;
      case 'outlook':
        suggestions = [
          'Schedule requirement review meeting',
          'Create calendar reminder for milestone',
          'Find available time slots',
          'Generate meeting agenda'
        ];
        break;
      case 'windchill':
        suggestions = [
          'Analyze CAD change impact',
          'Review part approval status',
          'Check design revision history',
          'Validate configuration management'
        ];
        break;
      case 'database':
        suggestions = [
          'Query requirements by criticality',
          'Find orphaned requirements',
          'Generate traceability matrix',
          'Analyze requirement metrics'
        ];
        break;
      default:
        if (body.include_requirements) {
          suggestions = [
            'Filter requirements by status',
            'Show critical requirements (DAL-A/B)',
            'Search for specific requirement',
            'Generate requirements report'
          ];
        } else {
          suggestions = [
            'Help me understand requirements traceability',
            'Show me system capabilities',
            'Explain impact analysis',
            'Guide me through the interface'
          ];
        }
    }

    return NextResponse.json({
      message: aiMessage,
      timestamp: new Date().toISOString(),
      context_used: {
        context_type: body.context_type,
        context_id: body.context_id,
        include_requirements: body.include_requirements
      },
      suggestions: suggestions
    });

  } catch (error) {
    console.error('AI chat error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}