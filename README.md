# YogaFlow

A modern yoga application designed to help users build and maintain their yoga practice.

## Project Structure

```
yogaflow/
├── frontend/
│   └── yogafrontend/    # React TypeScript frontend application
├── backend/             # Backend API and server
├── scripts/             # Build and deployment scripts
└── README.md
```

##Features TODO
- **Session Timer**: Built-in timer for timed practices and meditation
- **Saving of Flows** - allow each user to save their flows and access them again
- **Image provider** - use web scraping to generate images to go along with flows, use relational DB to store, store list of non scraped flows and execute lambda to scrape each day to get image of non held poses

## Features when complete
- **Custom Routines**: Create and save personalized yoga sequences
- **Session Timer**: Built-in timer for timed practices and meditation
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## Getting Started

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend/yogafrontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open your browser and navigate to `http://localhost:3000`

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Follow the backend-specific setup instructions in the backend directory

## Available Scripts (Frontend)

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

**Happy practicing! 🧘‍♀️✨**
