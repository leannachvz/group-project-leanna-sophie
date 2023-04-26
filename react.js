import React, { useState } from "react";

function AudioPlayer(props) {
    const [isPlaying, setIsPlaying] = useState(false);

    const handlePlay = () => {
        setIsPlaying(true);
    };

    const handlePause = () => {
        setIsPlaying(false);
    };

    const handleSend = () => {
        // TODO: Send the recording data to another user or server
    };

    return (
        <div>
            <audio
                controls
                loop={false} // stop playing in a loop
                onPlay={handlePlay}
                onPause={handlePause}
                src={props.src}
            />
            <button onClick={handleSend}>Send to User</button> // send button
        </div>
    );
}

export default AudioPlayer;
