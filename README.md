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

2. Go to Project directory
  ```bash
  cd OpenTerra
3. Run the following commands for backend libraries installation
  ```bash
  cd Backend
  ```bash
  pip install fastapi uvicorn python-dotenv openai requests shapely sqlalchemy 

