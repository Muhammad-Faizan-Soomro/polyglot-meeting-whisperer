import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import ControlButtons from "./components/ControlButtons";
import StatsPanel from "./components/StatsPanel";
import TranscriptCard from "./components/TranscriptCard";
import SettingsModal from "./components/SettingsModal";
import AgentCard from "./components/AgentCard";
import useAudioRecording from "./hooks/useAudioRecording";
import { getLanguageOptions } from "./utils/translator";
import "./App.css";

// Reusable Components
import QuestionCard from "./components/QuestionCard";
import SummaryCard from "./components/SummaryCard.js";
import TopicCard from "./components/TopicCard";
import KeywordCard from "./components/KeywordCard";
import TranslatedCard from "./components/TranslatedCard";

const App = () => {
  const [transcript, setTranscript] = useState([]);
  const [translatedTranscript, setTranslatedTranscript] = useState([]);
  const [language, setLanguage] = useState("en");
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [sessionStart, setSessionStart] = useState(null);
  const [sessionDuration, setSessionDuration] = useState("00:00");
  const [selectedOriginalLang, setSelectedOriginalLang] = useState("english");
  const [selectedTranslatedLang, setSelectedTranslatedLang] =
    useState("spanish");

  const [questions, setQuestions] = useState([]);
  const [summary, setSummary] = useState("");
  const [topics, setTopics] = useState([]);
  const [keywords, setKeywords] = useState([]);

  const { isRecording, isLoading, toggleRecording } = useAudioRecording({
    language,
    onSessionStart: () => setSessionStart(Date.now()),

    onTranscriptUpdate: (newData) => {
      setTranscript((prev) => [...prev, ...newData]);
    },

    onTranslatedUpdate: (text) => {
      setTranslatedTranscript((prev) => [
        ...prev,
        {
          speaker: "",
          text,
          time: new Date().toLocaleTimeString(),
        },
      ]);
    },

    onSummaryUpdate: (cleanSummary, topic) => {

      // 📝 Set summary
      setSummary(cleanSummary);

      // 🏷️ Append topic only if new
      setTopics((prev) => [...prev, topic]);
    },

    onQuestionsUpdate: (incomingQuestions) => {
      setQuestions((prev) => [...prev, ...incomingQuestions]); // ✅ Append questions
    },

    onKeywordsUpdate: (incomingKeywords) => {
      setKeywords((prev) => [...prev, ...incomingKeywords]); // ✅ Append keywords
    },
  });

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      if (sessionStart) {
        const elapsed = Math.floor((Date.now() - sessionStart) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        setSessionDuration(
          `${minutes.toString().padStart(2, "0")}:${seconds
            .toString()
            .padStart(2, "0")}`
        );
      }
    }, 1000);
    return () => clearInterval(timer);
  }, [sessionStart]);

  const summaryStats = {
    wordCount: transcript.reduce(
      (acc, curr) => acc + curr.text.split(" ").length,
      0
    ),
    speakers: [...new Set(transcript.map((t) => t.speaker))].length,
    avgWords: transcript.length
      ? transcript.reduce((acc, curr) => acc + curr.text.split(" ").length, 0) /
        [...new Set(transcript.map((t) => t.speaker))].length
      : 0,
  };

  const resetTranscript = () => {
    setTranscript([]);
    setTranslatedTranscript([]);
    setQuestions([]);
    setSummary("");
    setTopics([]);
    setKeywords([]);
    setSessionStart(null);
    setSessionDuration("00:00");
  };

  const handleExport = () => {
    const data = {
      session: {
        duration: sessionDuration,
        timestamp: new Date().toISOString(),
        summary: summaryStats,
      },
      original: transcript,
      translated: translatedTranscript,
      questions,
      summary,
      topics,
      keywords,
    };
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `meeting-transcript-${
      new Date().toISOString().split("T")[0]
    }.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const languageOptions = getLanguageOptions();

  const agents = [
    {
      icon: "🎤",
      title: "Audio Input Listener",
      description:
        "Captures and processes live audio input from meetings and conferences with advanced noise filtering",
      status: "Ready",
    },
    {
      icon: "📝",
      title: "Transcriber Agent",
      description:
        "Real-time speech-to-text using advanced recognition models (Groq/Whisper) with speaker identification",
      status: "Ready",
    },
    {
      icon: "🌍",
      title: "Translator Agent",
      description:
        "Live translation into multiple languages with contextual understanding and cultural nuances",
      status: "Ready",
    },
    {
      icon: "❓",
      title: "Question Generator Agent",
      description:
        "Generates relevant follow-up questions based on ongoing conversation to enhance engagement",
      status: "Ready",
    },
    {
      icon: "📋",
      title: "Summarizer Agent",
      description:
        "Continuously produces concise summaries of meeting content with key points and action items",
      status: "Ready",
    },
    {
      icon: "🏷",
      title: "Topic Extractor Agent",
      description:
        "Identifies and extracts major topics being discussed in real-time for categorization",
      status: "Ready",
    },
    {
      icon: "💡",
      title: "Keyword Explanation Agent",
      description:
        "Detects technical terms and provides brief explanations and definitions for better understanding",
      status: "Ready",
    },
    {
      icon: "🎯",
      title: "Output Orchestrator",
      description:
        "Coordinates and manages all agent outputs for seamless user experience and data flow",
      status: "Ready",
    },
  ];

  return (
    <div className="min-h-screen purple-gradient">
      <div className="container mx-auto px-4 py-6">
        <Header currentTime={currentTime} />
        <ControlButtons
          isRecording={isRecording}
          toggleRecording={toggleRecording}
          openSettings={() => setIsSettingsOpen(true)}
          resetTranscript={resetTranscript}
          exportData={handleExport}
        />
        <StatsPanel
          wordCount={summaryStats.wordCount}
          speakerCount={summaryStats.speakers}
          avgWords={summaryStats.avgWords}
          sessionDuration={sessionDuration}
        />
        <div className="grid grid-cols-2 gap-6 mb-6">
          <TranscriptCard transcript={transcript} isLoading={isLoading} />
          <TranslatedCard
            transcript={translatedTranscript}
            isLoading={isLoading}
          />
        </div>
        <div className="grid grid-cols-2 gap-6 mb-6">
          <QuestionCard questions={questions} isLoading={isLoading} />
          <SummaryCard summary={summary} isLoading={isLoading} />
        </div>
        <div className="grid grid-cols-2 gap-6 mb-6">
          <TopicCard topics={topics} isLoading={isLoading} />
          <KeywordCard keywords={keywords} isLoading={isLoading} />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {agents.map((agent, index) => (
            <AgentCard key={index} {...agent} />
          ))}
        </div>
        <SettingsModal
          isOpen={isSettingsOpen}
          onClose={() => setIsSettingsOpen(false)}
          language={language}
          onLanguageChange={setLanguage}
        />
      </div>
    </div>
  );
};

export default App;
