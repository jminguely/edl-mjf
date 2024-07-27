from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import xml.etree.ElementTree as ET
from collections import defaultdict

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

    # List to store (duration, clipitem_id, file_id) tuples
    clipitem_durations = []

    # Dictionary to store cumulative durations for each src-* file ID
    cumulative_durations = defaultdict(int)

    # Iterate through clipitems to collect durations and IDs
    for clipitem in clipitems:
        duration_element = clipitem.find('duration')
        file_id_element = clipitem.find('.//file')
        if duration_element is not None and duration_element.text.isdigit() and file_id_element is not None:
            duration = int(duration_element.text)
            clipitem_id = clipitem.get('id')
            file_id = file_id_element.get('id')
            clipitem_durations.append((duration, clipitem_id, file_id))
            if file_id.startswith('src-'):
                cumulative_durations[file_id] += duration

    # Sort the list by duration in descending order
    clipitem_durations.sort(reverse=True, key=lambda x: x[0])

    # Prepare the output data
    top_longest_cuts = [
        {
            "cut": clipitem_id.replace('cs-', ''),
            "cam": file_id.replace('src-', ''),
            "duration": frames_to_timecode(duration, frame_rate)
        }
        for duration, clipitem_id, file_id in clipitem_durations[:5]
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

@app.route('/edlstats', methods=['GET'])
def edlstats():
    file_name = request.args.get('concert', '2024-07-07_LAC_EDITORS')
    xml_file_path = f'data/{file_name}_EDL.xml'
    data = parse_edl(xml_file_path, frame_rate)
    return jsonify(data)

@app.route('/edlsummary', methods=['GET'])
def edlsummary():
    data_directory = 'data'
    total_duration = 0
    total_cuts = 0
    cuts_per_minute = 0

    concerts = [];

    for filename in os.listdir(data_directory):
        if filename.endswith('.xml'):
            filepath = os.path.join(data_directory, filename)
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

            longest_cut = max(clipitem_durations, key=lambda x: x[0])

            duration, clipitem_id, file_id = longest_cut

            top_longest_cut = {
                "cut": clipitem_id.replace('cs-', ''),
                "cam": file_id.replace('src-', ''),
                "duration": frames_to_timecode(duration, frame_rate)
            }

            total_duration_minutes = (clip_master_duration_frames / frame_rate) / 60 if clip_master_duration_frames is not None else 0

            cuts_per_minute = round(total_cuts / total_duration_minutes, 1) if total_duration_minutes > 0 else 0

            concerts.append( {
                "filename": filename,
                "clip_master_duration": clip_master_duration,
                "total_cuts": total_cuts,
                "cuts_per_minute": cuts_per_minute,
                "top_longest_cut_duration": top_longest_cut['duration'],
                "top_longest_cut_cam": top_longest_cut['cam'],
            })

    concerts = sorted(concerts, key=lambda x: x['filename'])
    return jsonify(concerts)

if __name__ == '__main__':
    app.run(debug=True)
