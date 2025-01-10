// Function to load and parse CSV file
function loadCSV() {
    Papa.parse("popular_songs.csv", {
        download: true,
        header: true,
        complete: function(results) {
            window.songData = results.data;
        }
    });
}


document.getElementById("genre").addEventListener("change", function() {
    const genre = this.value;
    displaySongs(genre);
});

// Function to display songs based on selected genre
function displaySongs(genre) {
    const songList = document.getElementById("songList");
    songList.innerHTML = ""; // Clear previous list

    if (!window.songData) return;

    // Filter songs by selected genre
    const filteredSongs = window.songData.filter(song => song.genre === genre);

    // Display filtered songs
    filteredSongs.forEach(song => {
        const li = document.createElement("li");
        li.textContent = song.name; // Assuming CSV has a 'title' column for song names
        songList.appendChild(li);
    });
}