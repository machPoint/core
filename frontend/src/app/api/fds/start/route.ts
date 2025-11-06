import { NextRequest, NextResponse } from 'next/server';
import { spawn } from 'child_process';
import path from 'path';

// Store process references globally (in production, you'd use a proper process manager)
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
    
    // Path to the FDS directory
    const fdsPath = path.join(process.cwd(), '..', 'backend', 'fds');
    
    // Check if already running
    if (runningProcesses.has('fds')) {
      return NextResponse.json(
        { error: 'Fake Data Service is already running' },
        { status: 409 }
      );
    }

    // Start the FDS process
    const fdsProcess = spawn('python', ['start_fds.py'], {
      cwd: fdsPath,
      detached: true,
      stdio: ['ignore', 'pipe', 'pipe']
    });

    // Store the process
    runningProcesses.set('fds', fdsProcess);

    // Handle process events
    fdsProcess.on('error', (error) => {
      console.error('FDS Process error:', error);
      runningProcesses.delete('fds');
    });

    fdsProcess.on('exit', (code) => {
      console.log(`FDS Process exited with code ${code}`);
      runningProcesses.delete('fds');
    });

    // Give it a moment to start
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Check if process is still running
    if (fdsProcess.killed) {
      return NextResponse.json(
        { error: 'Failed to start Fake Data Service' },
        { status: 500 }
      );
    }

    return NextResponse.json({
      success: true,
      message: 'Fake Data Service started successfully',
      processId: fdsProcess.pid?.toString(),
      port: 4000
    });

  } catch (error) {
    console.error('Error starting FDS:', error);
    return NextResponse.json(
      { 
        error: 'Failed to start Fake Data Service',
        details: error instanceof Error ? error.message : 'Unknown error',
        instructions: 'Please run "python start_fds.py" manually in the backend/fds directory'
      },
      { status: 500 }
    );
  }
}

export async function GET() {
  // Return status of running processes
  const runningProcesses = getProcessMap();
  const fdsRunning = runningProcesses.has('fds');
  return NextResponse.json({
    fdsRunning,
    processCount: runningProcesses.size
  });
}
