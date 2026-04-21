from yt_dlp import YoutubeDL

def parse(url):
    with YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        clist = ['title', 'id', 'description', 'ext', 'duration_string', 'filesize_approx', 'webpage_url']
        llist = [{info['thumbnail']}]
        if info.get("_type") is not None:
            for i in info.get("entries"):
                llist.append({j:k for j,k in i.items() if j in clist})
        else:
            llist.append({j:k for j,k in info.items() if j in clist})
        print(llist)
        return llist