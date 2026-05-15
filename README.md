# FioBot

FioBot is a project for the LARC VSSS 2026 (IEEE Very Small Size Soccer) competition.
The project aims to build a team of 6 mini soccer robots (3 main + 3 spares) controlled by a centralized strategy system that communicates over ESP-NOW and UDP multicast.

## Project Structure

The project is structured as a monorepo containing:
- **web/**: Frontend dashboard (HTML/CSS/JS) to monitor and control the robots.
- **strategy/**: Backend Python system built with FastAPI and Uvicorn. Implements game strategies and handles UDP communication with the simulator.
- **firmware/**: C/C++ firmware built with PlatformIO for ESP32 bridges and ESP32-C3 robots.
- **proto/**: Protobuf definitions.
- **docs/**: Project specifications and implementation plans.
- **scripts/**: Utility scripts, such as generating Python code from proto files.

## Communication Architecture

The system supports a Dual Mode operation (Sim/Real):
- **Simulator Mode**: FIRASim / VSS Vision publishes Environment data via UDP Multicast (`224.0.0.1:10002`). The Python backend receives it, computes strategies, and sends Commands via UDP (`127.0.0.1:20011`).
- **Real Mode**: The backend computes strategies and sends commands via USB Serial to an ESP32 Bridge, which relays the data via ESP-NOW to ESP32-C3 robots.
- **Dashboard**: A Web GUI connects to the Python backend via WebSocket (`ws://localhost:8000/ws`) to visualize the game and control settings.

## Hardware Specifications

- **Microcontroller**: ESP32-C3 per robot. ESP32 for the Bridge.
- **Dimensions**: Max 8.0 cm x 8.0 cm x 8.0 cm (LARC 2026 rules).
- **Communication Protocol**: ESP-NOW for Bridge -> Robot.
- **Vision System**: VSS Vision Software with a 1080p Webcam.

## Setup and Running

1. **Install Python dependencies:**
   The Python backend uses `uv`. Ensure `uv` is installed, then run:
   ```bash
   cd strategy
   uv sync
   ```

2. **Generate Protobuf Code:**
   You can generate the Python protobuf bindings by running:
   ```bash
   make proto
   ```

3. **Run the Development Server:**
   Start the FastAPI development server with:
   ```bash
   make dev
   ```

## Development and Features

- The logic is broken down into incremental phases defined in `docs/implementation_plan.md`.
- See `docs/project_spec.md` for more complete hardware, communication, and system requirements.
