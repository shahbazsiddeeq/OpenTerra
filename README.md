# OpenTerra - 3D Polygon Drawing Tool (Prototype)
Prototype software tool that enables users to design green roofs and manage water resources efficiently. The tool will feature a 3D interface for drawing polygon areas, backend support for data management, and a chatbot interface for user interaction.

## Project Structure
The project structure is organized as follows:
- `Frontend/`:
  - `src/`: Contains the source code of the Vue.js frontend application.
    - `assets/`: Containts assets.
    - `components/`: Contains Vue components.
    - `App.vue`: Main Vue application component.
  - `public/`: Contains static assets.
  - `index.html`
  - `package.json`
- `Backend/`
  - `App/`: Contains the source of FastAPI framework
    - `main.py`: main file of API checkpoints
    - `models.py`: sqlite db mthods
    - `test.db`: sqlite db
  - `.env` 
- `README.md`: This file.

## Installation and Setup
To run the project locally, follow these steps:

1. Clone the repository or download diorectly from the browser:
   ```bash
   git clone https://github.com/shahbazsiddeeq/OpenTerra.git

2. First go to Backend directory:
    ```bash
    cd OpenTerra/Backend

3. Run the following commands in backend directory for libraries installation:
    ```bash
    pip install fastapi uvicorn python-dotenv openai requests shapely sqlalchemy

4. Run the following command for backend run in App directory:
    ```bash
    cd app
    python -m uvicorn main:app --reload

5. Now it's time to load interface:
    First go to Frontend directory
    ```bash
    cd ../../Frontend
6. now run npm command if npm is not installed in your system then first install npm in your system (https://docs.npmjs.com/downloading-and-installing-node-js-and-npm):
    ```bash
    npm install
    npm i three
    npm run dev
You will get Local URL: http://localhost:5173/
