from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from asgiref.wsgi import WsgiToAsgi
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

app = FastAPI()
asgi_app = WsgiToAsgi(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frame_rate = 25

# Function to convert frames to HH:MM:SS:FF
def frames_to_timecode(frames, frame_rate):
    seconds = frames // frame_rate
    frames = frames % frame_rate
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

def get_clip_master_duration(root):
    # Find the clip element with id="clip-master"
    clip_master = root.find(".//clip[@id='clip-master']")
    # Extract the duration value
    if clip_master is not None:
        duration = clip_master.find('duration').text
        return int(duration)  # Convert to integer
    else:
        return None

def parse_edl(xml_file_path, frame_rate):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Extract people information
    people_element = root.find('.//people')
    if people_element is not None:
        people = {child.tag: child.text for child in people_element}
    else:
        people = {}

    # Extract clip-master duration
    clip_master_duration_frames = get_clip_master_duration(root)
    clip_master_duration = frames_to_timecode(clip_master_duration_frames, frame_rate) if clip_master_duration_frames is not None else "clip-master not found"

    # Find the clipitem elements within the specified path
    clipitems = root.findall('.//project/children/sequence/media/video/track/clipitem')

    # List to store (duration, clipitem_id, file_id, start_time) tuples
    clipitem_durations = []

    # Dictionary to store cumulative durations for each src-* file ID
    cumulative_durations = defaultdict(int)

    # Iterate through clipitems to collect durations, IDs, and start times
    for clipitem in clipitems:
        duration_element = clipitem.find('duration')
        start_element = clipitem.find('start')
        file_id_element = clipitem.find('.//file')
        if duration_element is not None and duration_element.text.isdigit() and file_id_element is not None and start_element is not None:
            duration = int(duration_element.text)
            start_time = int(start_element.text)
            clipitem_id = clipitem.get('id')
            file_id = file_id_element.get('id')
            clipitem_durations.append((duration, clipitem_id, file_id, start_time))
            if file_id.startswith('src-'):
                cumulative_durations[file_id] += duration

    # Sort the list by duration in descending order
    clipitem_durations.sort(reverse=True, key=lambda x: x[0])

    # Prepare the output data
    top_longest_cuts = [
        {
            "cut": clipitem_id.replace('cs-', ''),
            "cam": file_id.replace('src-', ''),
            "duration": frames_to_timecode(duration, frame_rate),
            "start_timecode": frames_to_timecode(start_time, frame_rate)
        }
        for duration, clipitem_id, file_id, start_time in clipitem_durations[:5]
    ]

    sorted_cumulative_durations = sorted(cumulative_durations.items(), key=lambda x: x[1], reverse=True)

    total_durations = [
        {
            "cam": file_id.replace('src-', ''),
            "total_duration": frames_to_timecode(total_duration, frame_rate)
        }
        for file_id, total_duration in sorted_cumulative_durations
    ]

    total_cuts = len(clipitems)

    # Calculate the total duration in minutes
    total_duration_minutes = (clip_master_duration_frames / frame_rate) / 60 if clip_master_duration_frames is not None else 0

    # Calculate cuts per minute
    cuts_per_minute = round(total_cuts / total_duration_minutes, 1) if total_duration_minutes > 0 else 0

    return {
        "top_longest_cuts": top_longest_cuts,
        "total_durations": total_durations,
        "people": people,
        "clip_master_duration": clip_master_duration,
        "total_cuts": total_cuts,
        "cuts_per_minute": cuts_per_minute
    }

@app.get("/edlstats")
async def edlstats(request: Request):
    file_name = request.query_params.get('concert', '2024-07-07_LAC_EDITORS')
    try:
        # Extract year from filename
        year = file_name.split('-')[0]
        xml_file_path = f'data/{year}/{file_name}_EDL.xml'

        # Check if file exists
        if not os.path.exists(xml_file_path):
            return {"error": f"File not found: {xml_file_path}"}

        data = parse_edl(xml_file_path, frame_rate)
        return data
    except Exception as e:
        return {"error": f"Error processing file: {str(e)}"}

@app.get("/edlsummary")
def edlsummary():
    data_directory = 'data'
    concerts = []

    try:
        # Iterate through year folders
        for year_folder in sorted(os.listdir(data_directory)):
            year_path = os.path.join(data_directory, year_folder)
            if os.path.isdir(year_path):
                for filename in sorted(os.listdir(year_path)):
                    if filename.endswith('.xml'):
                        try:
                            filepath = os.path.join(year_path, filename)
                            tree = ET.parse(filepath)
                            root = tree.getroot()

                            # Check and extract elements safely
                            clip_master_duration_frames = get_clip_master_duration(root)
                            clip_master_duration = frames_to_timecode(clip_master_duration_frames, frame_rate) if clip_master_duration_frames is not None else "clip-master not found"

                            clipitems = root.findall('.//project/children/sequence/media/video/track/clipitem')
                            total_cuts = len(clipitems)

                            clipitem_durations = []
                            # Iterate through clipitems to collect durations and IDs
                            for clipitem in clipitems:
                                duration_element = clipitem.find('duration')
                                file_id_element = clipitem.find('.//file')
                                if duration_element is not None and duration_element.text.isdigit() and file_id_element is not None:
                                    duration = int(duration_element.text)
                                    clipitem_id = clipitem.get('id')
                                    file_id = file_id_element.get('id')
                                    clipitem_durations.append((duration, clipitem_id, file_id))

                            if clipitem_durations:
                                longest_cut = max(clipitem_durations, key=lambda x: x[0])
                                duration, clipitem_id, file_id = longest_cut
                                top_longest_cut = {
                                    "cut": clipitem_id.replace('cs-', ''),
                                    "cam": file_id.replace('src-', ''),
                                    "duration": frames_to_timecode(duration, frame_rate)
                                }
                            else:
                                top_longest_cut = {
                                    "cut": "N/A",
                                    "cam": "N/A",
                                    "duration": "00:00:00:00"
                                }

                            total_duration_minutes = (clip_master_duration_frames / frame_rate) / 60 if clip_master_duration_frames is not None else 0
                            cuts_per_minute = round(total_cuts / total_duration_minutes, 1) if total_duration_minutes > 0 else 0

                            concerts.append({
                                "filename": filename,
                                "year": year_folder,
                                "clip_master_duration": clip_master_duration,
                                "total_cuts": total_cuts,
                                "cuts_per_minute": cuts_per_minute,
                                "top_longest_cut_duration": top_longest_cut['duration'],
                                "top_longest_cut_cam": top_longest_cut['cam'],
                            })
                        except Exception as e:
                            print(f"Error processing {filename}: {e}")
                            continue

        concerts = sorted(concerts, key=lambda x: x['filename'])
        return concerts
    except Exception as e:
        print(f"Error in edlsummary: {e}")
        return {"error": f"Error processing summary: {str(e)}"}

@app.get("/concerts")
def get_concerts():
    data_directory = 'data'
    concerts = []

    # Iterate through year folders
    try:
        for year_folder in sorted(os.listdir(data_directory)):
            year_path = os.path.join(data_directory, year_folder)
            if os.path.isdir(year_path):
                for filename in sorted(os.listdir(year_path)):
                    if filename.endswith('.xml'):
                        # Remove the _EDL.xml suffix to get the concert name
                        concert_name = filename.replace('_EDL.xml', '')
                        concerts.append({
                            "name": concert_name,
                            "year": year_folder,
                            "filename": filename
                        })
    except Exception as e:
        print(f"Error reading concerts: {e}")
        return {"error": "Could not read concerts data"}

    # Sort by name (which includes date)
    concerts = sorted(concerts, key=lambda x: x['name'])
    return concerts

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
