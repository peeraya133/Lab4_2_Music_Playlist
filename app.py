import streamlit as st

# --- Song Class ---
class Song:
    def __init__(self, title, artist, audio_bytes=None, audio_type=None):
        self.title = title
        self.artist = artist
        self.audio_bytes = audio_bytes
        self.audio_type = audio_type
        self.next_song = None

    def __str__(self):
        return f"{self.title} by {self.artist}"


# --- MusicPlaylist Class ---
class MusicPlaylist:
    def __init__(self):
        self.head = None
        self.current_song = None
        self.length = 0

    def add_song(self, title, artist, audio_bytes=None, audio_type=None):
        new_song = Song(title, artist, audio_bytes, audio_type)
        if self.head is None:
            self.head = new_song
            self.current_song = new_song
        else:
            current = self.head
            while current.next_song:
                current = current.next_song
            current.next_song = new_song

        self.length += 1
        st.success(f"Added: {new_song}")

    def display_playlist(self):
        songs = []
        current = self.head
        count = 1
        while current:
            marker = "▶️ " if current == self.current_song else ""
            songs.append(f"{marker}{count}. {current.title} by {current.artist}")
            current = current.next_song
            count += 1
        return songs

    def play_current_song(self):
        if self.current_song:
            st.info(f"Now playing: {self.current_song}")
            if self.current_song.audio_bytes:
                st.audio(
                    self.current_song.audio_bytes,
                    format=self.current_song.audio_type
                )
        else:
            st.warning("Playlist is empty or no song selected.")

    def next_song(self):
        if self.current_song and self.current_song.next_song:
            self.current_song = self.current_song.next_song
        else:
            st.warning("End of playlist.")

    def prev_song(self):
        if self.current_song == self.head:
            st.warning("Already at first song.")
            return

        current = self.head
        while current and current.next_song != self.current_song:
            current = current.next_song

        if current:
            self.current_song = current

    def delete_song(self, title):
        if not self.head:
            st.error("Playlist is empty.")
            return

        if self.head.title == title:
            self.head = self.head.next_song
            self.current_song = self.head
            self.length -= 1
            return

        prev = self.head
        current = self.head.next_song

        while current:
            if current.title == title:
                prev.next_song = current.next_song
                if self.current_song == current:
                    self.current_song = prev
                self.length -= 1
                st.success(f"Deleted: {title}")
                return
            prev = current
            current = current.next_song

        st.error("Song not found.")

    def get_length(self):
        return self.length


# --- Streamlit UI ---
st.title("🎶 Music Playlist App")

if "playlist" not in st.session_state:
    st.session_state.playlist = MusicPlaylist()

# --- Sidebar: Add Song ---
st.sidebar.header("Add New Song")
title = st.sidebar.text_input("Title")
artist = st.sidebar.text_input("Artist")

audio_file = st.sidebar.file_uploader(
    "🎵 Upload Audio File",
    type=["mp3", "wav", "ogg"]
)

if audio_file:
    st.sidebar.success(f"Loaded: {audio_file.name}")


if st.sidebar.button("Add Song to Playlist"):
    if title and artist:
        audio_bytes = audio_file.read() if audio_file else None
        audio_type = audio_file.type if audio_file else None
        st.session_state.playlist.add_song(
            title, artist, audio_bytes, audio_type
        )
    else:
        st.sidebar.warning("Please enter title and artist.")

# --- Sidebar: Delete ---
st.sidebar.header("Delete Song")
delete_title = st.sidebar.text_input("Song Title to Delete")
if st.sidebar.button("Delete Song"):
    st.session_state.playlist.delete_song(delete_title)

# --- Playlist Display ---
st.header("Your Current Playlist")
playlist = st.session_state.playlist.display_playlist()
if playlist:
    for song in playlist:
        st.write(song)
else:
    st.write("Playlist is empty.")

# --- Controls ---
st.header("Playback Controls")
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("⏪ Previous"):
        st.session_state.playlist.prev_song()
        st.session_state.playlist.play_current_song()

with c2:
    if st.button("▶️ Play Current"):
        st.session_state.playlist.play_current_song()

with c3:
    if st.button("⏩ Next"):
        st.session_state.playlist.next_song()
        st.session_state.playlist.play_current_song()

st.markdown("---")
st.write(f"Total songs: {st.session_state.playlist.get_length()}")
