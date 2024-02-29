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

1. Clone the repository:
   ```bash
   git clone https://github.com/shahbazsiddeeq/OpenTerra.git
