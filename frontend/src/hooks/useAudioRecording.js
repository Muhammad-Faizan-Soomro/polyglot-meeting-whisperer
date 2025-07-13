// hooks/useAudioRecording.js
import { useState, useRef, useEffect } from "react";

const useAudioRecording = ({
  onTranscriptUpdate,
  onTranslatedUpdate,
  onSummaryUpdate,
  onQuestionsUpdate,
  onKeywordsUpdate,
  onSessionStart,
  language,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const socketRef = useRef(null);
  const mediaStreamRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    // Connect WebSocket on mount
    socketRef.current = new WebSocket("ws://localhost:8765");

    socketRef.current.onopen = () => {
      console.log("✅ WebSocket connected.");
    };

    socketRef.current.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);

        switch (message.type) {
          case "transcript":
            onTranscriptUpdate?.([
              {
                speaker: "Speaker",
                text: message.data,
                time: new Date().toLocaleTimeString(),
              },
            ]);
            break;

          case "translated":
            onTranslatedUpdate?.(message.data);
            break;

          case "summary":
            const rawSummary = message.data;
            const topicMatch = rawSummary.match(/- Topic:\s*(.+)/);
            const topic = topicMatch ? topicMatch[1].trim() : null;

            // Extract clean summary (strip topic line)
            const cleanSummary = rawSummary.split("- Topic:")[0].trim();

            if (onSummaryUpdate) {
              onSummaryUpdate(cleanSummary, topic);
            }
            break;

          case "questions":
            onQuestionsUpdate?.(message.data.map((q) => ({ text: q })));
            break;

          case "keywords":
            onKeywordsUpdate?.(
              message.data.map((kw) => ({
                term: kw.keyword,
                explanation: kw.definition,
              }))
            );
            break;

          default:
            console.warn("⚠️ Unknown message type:", message.type);
        }
      } catch (err) {
        console.error("❌ Failed to parse WebSocket message:", err);
      }
    };

    socketRef.current.onerror = (err) => {
      console.error("❌ WebSocket error:", err);
    };

    socketRef.current.onclose = (event) => {
      console.log(
        `❌ WebSocket closed. Code: ${event.code}, Reason: ${event.reason}`
      );
    };

    return () => {
      socketRef.current?.close();
    };
  }, []);

  useEffect(() => {
    if (isRecording) {
      startRecording();
    } else {
      stopRecording();
    }
  }, [isRecording]);

  const recordChunk = () => {
    const recorder = new MediaRecorder(mediaStreamRef.current, {
      mimeType: "audio/webm;codecs=opus",
    });

    recorder.ondataavailable = (event) => {
      if (
        event.data.size > 0 &&
        socketRef.current?.readyState === WebSocket.OPEN
      ) {
        socketRef.current.send(event.data);
        console.log("📤 Sent audio chunk:", event.data.size);
      }
    };

    recorder.start();

    setTimeout(() => {
      if (recorder.state !== "inactive") {
        recorder.stop();
      }
    }, 5000); // 5 seconds per chunk
  };

  const startRecording = async () => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      alert("WebSocket not connected!");
      return;
    }

    // 🛠️ Send config including language
    socketRef.current.send(
      JSON.stringify({
        type: "config",
        language,
      })
    );

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaStreamRef.current = stream;
      setIsLoading(true);

      if (onSessionStart) onSessionStart();

      recordChunk(); // Send first chunk

      intervalRef.current = setInterval(() => {
        if (isRecording) {
          recordChunk();
        }
      }, 5000);

      console.log("🎙️ Recording started.");
      setIsLoading(false);
    } catch (err) {
      console.error("🎤 Error accessing microphone:", err);
      setIsLoading(false);
    }
  };

  const stopRecording = () => {
    clearInterval(intervalRef.current);
    intervalRef.current = null;

    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }

    console.log("🛑 Recording stopped.");
  };

  const toggleRecording = () => {
    setIsRecording((prev) => !prev);
  };

  return {
    isRecording,
    isLoading,
    toggleRecording,
  };
};

export default useAudioRecording;
