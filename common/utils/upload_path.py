

def file_upload_path(instance, filename):
    folder = 'files'

    # if isinstance(instance, Song):
    #     folder = 'songs'
    # elif isinstance(instance, StudioEpisode):
    #     folder = 'episodes'

    return '{0}/{1}'.format(folder, filename)
