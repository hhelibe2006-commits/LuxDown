from yt_dlp import YoutubeDL
def parse(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        list = ['title', 'description', 'id', 'ext', 'duration_string', 'filesize_approx', 'webpage_url', 'thumbnail']
        llist = []
        if info.get("_type") != None:
            for i in info.get("entries"):
                llist.append({j:k for j,k in i.items() if j in list})
        else:
            llist.append({j:k for j,k in info.items() if j in list})
        return llist