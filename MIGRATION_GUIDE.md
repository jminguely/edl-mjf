# MJF EDL Stats

A web application for analyzing EDL (Edit Decision List) files from the Montreux Jazz Festival. The application provides statistical analysis of concert recordings, including cut analysis, camera usage, and timing information.

## Project Structure

```
edl-mjf/
├── api/                    # FastAPI backend
│   ├── app.py             # Main API application
│   ├── requirements.txt   # Python dependencies
│   └── data/              # EDL XML files organized by year
│       ├── 2024/          # 2024 concert files
│       └── 2025/          # 2025 concert files
├── app/                   # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── data/         # Static data files
│   │   └── router/       # Vue router configuration
│   └── package.json      # Node.js dependencies
└── test_api.py           # API testing script
```

## Features

### API Endpoints

- **GET /concerts** - Returns a list of all available concerts with year information
- **GET /edlstats?concert={concert_name}** - Returns detailed statistics for a specific concert
- **GET /edlsummary** - Returns summary statistics for all concerts

### Frontend Features

- **Concert Details View** - Detailed analysis of individual concerts including:

  - General statistics (duration, total cuts, cuts per minute)
  - Camera operator information
  - Top 5 longest cuts
  - Total duration per camera
  - Year-based filtering

- **Summary View** - Overview of all concerts with:
  - Sortable columns (concert name, year, duration, cuts, etc.)
  - Year-based filtering
  - Export capabilities

## Data Structure

The application now supports year-based organization of EDL files:

```
data/
├── 2024/
│   ├── 2024-07-05_CASINO_HENRY-MOODIE_EDL.xml
│   ├── 2024-07-05_CASINO_LAUREN-SPENCER-SMITH_EDL.xml
│   └── ...
└── 2025/
    ├── 2025-07-04_LAC_CHAKA-KHAN_EDL.xml
    ├── 2025-07-05_LAC_J-BALVIN_EDL.xml
    └── ...
```

## Installation & Setup

### API Setup

1. Navigate to the API directory:

   ```bash
   cd api
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the API server:

   ```bash
   python app.py
   ```

   The API will be available at `http://127.0.0.1:8000`

### Frontend Setup

1. Navigate to the app directory:

   ```bash
   cd app
   ```

2. Install Node.js dependencies:

   ```bash
   npm install
   ```

3. Start the development server:

   ```bash
   npm run serve
   ```

   The app will be available at `http://localhost:8080`

## Usage

### Adding New EDL Files

1. Place new EDL XML files in the appropriate year folder under `api/data/`
2. Follow the naming convention: `YYYY-MM-DD_VENUE_ARTIST_EDL.xml`
3. The system will automatically detect and process new files

### API Testing

Use the provided test script to verify API functionality:

```bash
python test_api.py
```

This will test all endpoints and verify the year-based structure is working correctly.

## API Documentation

### Concert Data Structure

Each concert object contains:

- `name`: Concert identifier (e.g., "2024-07-05_CASINO_HENRY-MOODIE")
- `year`: Year folder (e.g., "2024", "2025")
- `filename`: Original XML filename
- `clip_master_duration`: Total duration in HH:MM:SS:FF format
- `total_cuts`: Number of cuts in the concert
- `cuts_per_minute`: Average cuts per minute
- `top_longest_cut_duration`: Duration of the longest cut
- `top_longest_cut_cam`: Camera number for the longest cut

### EDL Statistics Structure

Detailed statistics include:

- `top_longest_cuts`: Array of the 5 longest cuts with camera and duration info
- `total_durations`: Array of total duration per camera
- `people`: Object mapping camera numbers to operator names
- `clip_master_duration`: Total concert duration
- `total_cuts`: Total number of cuts
- `cuts_per_minute`: Average cuts per minute

## Technical Details

### Backend (FastAPI)

- **Framework**: FastAPI with ASGI support
- **XML Processing**: ElementTree for parsing EDL files
- **CORS**: Configured for cross-origin requests
- **Error Handling**: Comprehensive error handling for file operations

### Frontend (Vue.js 3)

- **Framework**: Vue 3 with Composition API
- **HTTP Client**: Axios for API communication
- **Routing**: Vue Router for navigation
- **Styling**: PostCSS with custom styling

## Changes from Previous Version

### API Changes

1. **Year-based File Organization**: Files are now organized in year folders instead of a flat structure
2. **Enhanced Error Handling**: Better error responses for missing files and parsing errors
3. **New Concerts Endpoint**: Dynamic concert list generation from file system
4. **Improved Data Structure**: Added year information to all responses

### Frontend Changes

1. **Year Filtering**: Added year-based filtering in both detail and summary views
2. **Dynamic Concert Loading**: Concerts are now loaded dynamically from the API
3. **Enhanced UI**: Better organization with year information displayed
4. **Improved Error Handling**: Fallback to static data if API is unavailable

## Deployment

For production deployment:

1. **API**: Deploy using a WSGI server like Gunicorn or Uvicorn
2. **Frontend**: Build the production version with `npm run build`
3. **Static Files**: Serve the built files using a web server like Nginx

## Support

For issues or questions regarding the year-based structure adaptation, please refer to the test script (`test_api.py`) which demonstrates the expected API behavior.
