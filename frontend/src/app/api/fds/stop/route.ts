import { NextRequest, NextResponse } from 'next/server';

// Import the same process map from start route
// In a real app, you'd use a shared store or process manager
declare global {
  var runningProcesses: Map<string, any> | undefined;
}

const getProcessMap = () => {
  if (!global.runningProcesses) {
    global.runningProcesses = new Map();
  }
  return global.runningProcesses;
};

export async function POST(request: NextRequest) {
  try {
    const runningProcesses = getProcessMap();
    
    // Check if FDS is running
    if (!runningProcesses.has('fds')) {
      return NextResponse.json(
        { error: 'Fake Data Service is not running' },
        { status: 404 }
      );
    }

    const fdsProcess = runningProcesses.get('fds');
    
    // Kill the process
    if (fdsProcess && !fdsProcess.killed) {
      fdsProcess.kill('SIGTERM');
      
      // Give it time to shut down gracefully
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Force kill if still running
      if (!fdsProcess.killed) {
        fdsProcess.kill('SIGKILL');
      }
    }
    
    // Remove from running processes
    runningProcesses.delete('fds');

    return NextResponse.json({
      success: true,
      message: 'Fake Data Service stopped successfully'
    });

  } catch (error) {
    console.error('Error stopping FDS:', error);
    return NextResponse.json(
      { 
        error: 'Failed to stop Fake Data Service',
        details: error instanceof Error ? error.message : 'Unknown error',
        instructions: 'You may need to manually stop the process if it is still running'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  const runningProcesses = getProcessMap();
  return NextResponse.json({
    fdsRunning: runningProcesses.has('fds'),
    processCount: runningProcesses.size
  });
}