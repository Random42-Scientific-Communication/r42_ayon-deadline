"""
Custom Static Functions for R42 Use
"""
import os
import pprint

# ========================== R42 Custom ======================================

def get_job_settings(instance):
    """
    Get the user's input from collect_job settings
    """
    return instance.data['publish_attributes']['CollectJobInfo']

def get_r42_preview_settings(instance):
    """
    Get the user's input for R42's preview settings in the UI.
    """
    return instance.data['publish_attributes']['CollectR42JobInfo']

def get_houdini_submit_settings(instance):
    """
    Get the houdini specific submit settings
    """
    return instance.data['publish_attributes']['HoudiniSubmitDeadline']

def get_r42_preview_job_id(instance):
    return instance.data.get("previewDeadlineSubmissionJob")

def get_height_width(instance):
    height = instance.data["taskEntity"]["attrib"]["resolutionHeight"]
    width = instance.data["taskEntity"]["attrib"]["resolutionWidth"]
    return height, width

def modify_preview_json_data(instance, publish_job, log=None):
    """
    This modifies the json publish file to only ffmpeg and publish preview frames
    """
    r42_preview_attributes = get_r42_preview_settings(instance)
    preview_frame_skip = r42_preview_attributes["preview_frame_skip"]
    height, width = get_height_width(instance)

    if log:
        log.debug("==============BEFORE================")
        publish_job_data = pprint.pformat(publish_job)
        log.debug(publish_job_data)

    publish_instances = publish_job["instances"]
    for i in range(0, len(publish_instances)):
        publish_instance = publish_instances[i]
        publish_job["instances"][i]["resolutionHeight"] = height
        publish_job["instances"][i]["resolutionWidth"] = width
        rep = publish_instance["representations"]
        for r in range(0, len(rep)):
            out_file_list = rep[r]["files"]
            preview_file_list = []
            for f in range(0, len(out_file_list), preview_frame_skip):
                current_file = out_file_list[f]
                preview_file_list.append(current_file)
            publish_job["instances"][i]["representations"][r]["files"] = preview_file_list

    if log:
        log.debug("==============AFTER================")
        publish_job_data = pprint.pformat(publish_job)
        log.debug(publish_job_data)

    return publish_job

def modify_json_data(instance, publish_job):
    height, width = get_height_width(instance)

    publish_instances = publish_job["instances"]
    for i in range(0, len(publish_instances)):
        publish_job["instances"][i]["resolutionHeight"] = height
        publish_job["instances"][i]["resolutionWidth"] = width

    return publish_job

def modify_json_path(input_path, log=None):
    """
    This renames the json file that is meant to do a publish job, to add a preview after it
    Thus we have 2 json files, one for preview and one for publish
    """
    if log:
        log.debug("=============================")
        log.debug(f"input_path is {input_path}\n")
    basename = os.path.basename(input_path)
    splitext = os.path.splitext(basename)
    new_basename = f"{splitext[0]}_preview{splitext[1]}"
    new_path = os.path.join(os.path.dirname(input_path), new_basename)
    if log:
        log.debug("=============================")
        log.debug(f"new_path is {new_path}\n")
    return new_path

def get_non_preview_frames(instance):
    start = int(instance.data["frameStart"])
    end = int(instance.data["frameEnd"])
    skip = int(instance.data['preview_frame_skip'])

    preview_frames = []
    rest_of_frames = []

    for i in range(start, end + 1, skip):
        preview_frames.append(i)

    for i in range(start, end + 1):
        rest_of_frames.append(i)

    rest_of_frames = list(set(rest_of_frames) - set(preview_frames))
    rest_of_frames.sort()
    frame_str = ','.join([str(x) for x in rest_of_frames])
    return frame_str