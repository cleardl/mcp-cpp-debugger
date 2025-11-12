import asyncio
from typing import Optional

from fastmcp import FastMCP
from mcp_cpp_debugger.debugger.cdb import CDB_Session
cdb_session = CDB_Session()
server = FastMCP("cdb-debugger")

@server.tool()
async def launch( 
    executable_path:str,
    cdb_path: str="cdb.exe",
    arguments: str="",
    symbol_path: str="",
) -> str:
    """
    Start CDB debugger with specified parameters
    
    Args:
        cdb_path: Path to CDB executable (default: "cdb.exe")
        executable_path: Path to the executable file to debug
        source_path: Source code path
        symbol_path: Symbol file (.pdb) search path
        arguments: List of startup arguments for the executable
        debug_children: Whether to enable child process debugging
        
    Returns:
        str: Result message from CDB debugger startup
    """
    try:
        result = await asyncio.to_thread(
            cdb_session.launch,
            executable_path=executable_path,
            cdb_path=cdb_path,
            args=arguments,
            symbol_path=symbol_path,
        )
        return result
    except Exception as e: 
        return f"Error starting debugger: {str(e)}"

@server.tool()
async def analyze_dump(dump_file_path: str,symbol_path: str = "",cdb_path: str = "cdb.exe",source_path_map: dict[str,str] = {"*/Coding":"C:/Users/wps/workspace/master_kso_v12/Coding"}) -> str:
    """
    Analyze a dump file with specified parameter
    
    Args:
        dump_file_path: Path to the dump file to analyze
        symbol_path: Symbol file (.pdb) search path
    """
    try:
        result = await asyncio.to_thread(cdb_session.analyze_dump, dump_file_path,symbol_path,cdb_path,source_path_map)
        return result
    except Exception as e:
        return f"Error analyzing dump: {str(e)}"


@server.tool()
async def continue_execution() -> str:
    """
    Continue program execution,the command is 'g'
    
    Returns:
        str: Result message from continue operation
    """
    try:
        result = await asyncio.to_thread(cdb_session.continue_execution)
        return result
    except Exception as e:
        return f"Error continuing execution: {str(e)}"     

@server.tool()
async def terminate() -> str:
    """
    Terminate the CDB debug session
    
    Returns:
        str: Result message from terminate operation
    """
    try:
        result = await asyncio.to_thread(cdb_session.terminate)
        return result
    except Exception as e:
        return f"Error terminating CDB debug session: {str(e)}"

@server.tool()
async def execute_command(command: str) -> str:
    """
    Execute a CDB command
    
    Args:
        command: CDB command to execute
        
    Returns:
        str: Output from the CDB command
    """
    try:
        result = await asyncio.to_thread(cdb_session.execute_command, command)
        return result
    except Exception as e:
        return f"Error executing command '{command}': {str(e)}"

@server.tool()
async def set_breakpoint(
    file_path: str,
    line_number: int,
) -> str:
    """
    Set a breakpoint in CDB,the command is bp `{file_path}:{line_number}`
    
    Args:
        file_path: absolute file path
        line_number: Line number
        
    Returns:
        str: Result message from breakpoint setting
    """
    try:
        result = await asyncio.to_thread(
            cdb_session.set_breakpoint,
            file_path=file_path,
            line_number=line_number,
        )
        return result
    except Exception as e:
        return f"Error setting breakpoint: {str(e)}"

@server.tool()
async def enable_breakpoint(breakpoint_number: int) -> str:
    """
    Enable a breakpoint by number,the command is be {breakpoint_number}
    
    Args:
        breakpoint_number: Breakpoint number to enable
        
    Returns:
        str: Result message from breakpoint enabling
    """
    try:
        result = await asyncio.to_thread(cdb_session.enable_bp, breakpoint_number)
        return result
    except Exception as e:
        return f"Error enabling breakpoint {breakpoint_number}: {str(e)}"

@server.tool()
async def disable_breakpoint(breakpoint_number: int) -> str:
    """
    Disable a breakpoint by number,the command is bd {breakpoint_number}
    
    Args:
        breakpoint_number: Breakpoint number to disable
        
    Returns:
        str: Result message from breakpoint disabling
    """
    try:
        result = await asyncio.to_thread(cdb_session.disable_bp, breakpoint_number)
        return result
    except Exception as e:
        return f"Error disabling breakpoint {breakpoint_number}: {str(e)}"

@server.tool()
async def delete_breakpoint(breakpoint_number: int) -> str:
    """
    Delete a breakpoint by number,the command is bc {breakpoint_number}
    
    Args:
        breakpoint_number: Breakpoint number to delete
        
    Returns:
        str: Result message from breakpoint deletion
    """
    try:
        result = await asyncio.to_thread(cdb_session.delete_bp, breakpoint_number)
        return result
    except Exception as e:
        return f"Error deleting breakpoint {breakpoint_number}: {str(e)}"

@server.tool()
async def list_breakpoints() -> str:
    """
    List all breakpoints,the command is bl
    
    Returns:
        str: List of all breakpoints
    """
    try:
        result = await asyncio.to_thread(cdb_session.get_breakpoint_list)
        return result
    except Exception as e:
        return f"Error listing breakpoints: {str(e)}"

@server.tool()
async def get_stack_trace() -> str:
    """
    Get the current stack trace,the command is kv
    
    Returns:
        str: Stack trace information
    """
    try:
        result = await asyncio.to_thread(cdb_session.get_stack_trace)
        return result
    except Exception as e:
        return f"Error getting stack trace: {str(e)}"

@server.tool()
async def step_over() -> str:
    """
    Step over the current instruction,
    the command is p,
    may wait for the single step over or step out debugging to complete，
    but target program may be running a long time task,
    if wait timeout, will return "wait timeout, target program may be running,
    please wait for the running to complete",
    """
    return await asyncio.to_thread(cdb_session.step_over)

@server.tool()
async def step_into() -> str:
    """
    Step into the current instruction,the command is t
    
    Returns:
        str: Result message from step into operation
    """
    try:
        result = await asyncio.to_thread(cdb_session.step_into)
        return result
    except Exception as e:
        return f"Error stepping into: {str(e)}"

@server.tool()
async def step_out() -> str:
    """
    Step out of the current function,the command is gu
    
    Returns:
        str: Result message from step out operation
    """
    try:
        result = await asyncio.to_thread(cdb_session.step_out)
        return result
    except Exception as e:
        return f"Error stepping out: {str(e)}"

@server.tool()
async def interrupt_target_program() -> str:
    """
    Interrupt the target program being debugged (send CTRL_BREAK_EVENT to process group)
    
    This function sends an interrupt signal to the debugged program, causing it to pause
    and enter debugging state, without terminating the CDB debugger itself. 
    Equivalent to pressing Ctrl+C in CDB.
    
    Returns:
        str: Result message of the interrupt operation
    """
    try:
        result = await asyncio.to_thread(cdb_session.interrupt_target_program)
        return result
    except Exception as e:
        return f"Error interrupting target program: {str(e)}"

@server.tool()
async def get_debugger_status() -> str:
    """
    Get the current status of the debugger
    
    Returns:
        str: Current status of the debugger
        {
            "session_state": "UNSTARTED" | "RUNNING" | "TERMINATED",
            "debug_mode": "LAUNCH" | "ATTACH" | "DUMP_ANALYSIS",
            "start_cmdline": start command line,
            "executable_path": executable path, if debug mode is LAUNCH
            "target_process_state": target process state,if debug mode is LAUNCH or ATTACH
            "dump_file_path": dump file path, if debug mode is DUMP_ANALYSIS
        }
    
    """
    try:
        result = await asyncio.to_thread(cdb_session.get_current_status)
        return result
    except Exception as e:
        return f"Error getting debugger status: {str(e)}"

def main():
    import logging
    import traceback
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    try:

        server.run(transport="sse", port=8999)
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
    except Exception as e:
        logging.error(f"Error running server: {e}")
        logging.error(f"Full traceback: {traceback.format_exc()}")
    finally:
        logging.info("Server process ending")

if __name__ == "__main__":
    main()
