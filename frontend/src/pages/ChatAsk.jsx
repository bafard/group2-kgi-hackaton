import React, { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { generateReply, generateRAGReply } from '../lib/api';

/**
 * ChatAsk Component - A conversational chatbot interface
 * 
 * Features:
 * - Text input with submit button for user questions
 * - Maintains conversation history with context preservation
 * - Visual differentiation between user and bot messages
 * - Auto-scroll to latest messages
 * - Clear input after submission
 */
const ChatAsk = () => {
  // State for storing conversation history
  const [messages, setMessages] = useState([]);
  const [currentInput, setCurrentInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [useRAG, setUseRAG] = useState(true);
  const [contextInfo, setContextInfo] = useState(null);

  // Ref for auto-scrolling to bottom
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Focus input on component mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  /**
   * Handle form submission - add user message and get bot reply
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validate input
    if (!currentInput.trim() || isLoading) {
      return;
    }

    const userMessage = { role: 'user', content: currentInput.trim() };
    const updatedMessages = [...messages, userMessage];
    
    // Update state with user message
    setMessages(updatedMessages);
    setCurrentInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Call appropriate API based on RAG setting
      const response = useRAG 
        ? await generateRAGReply(updatedMessages)
        : await generateReply(updatedMessages);
      
      // Store context information for display
      if (response.context_summary) {
        setContextInfo(response.context_summary);
      }
      
      // Add bot response to conversation
      const botMessage = { 
        role: 'assistant', 
        content: response.response,
        contextInfo: response.context_summary
      };
      setMessages([...updatedMessages, botMessage]);
      
    } catch (err) {
      console.error('Error getting bot reply:', err);
      setError('Failed to get response. Please try again.');
      
      // Add error message to conversation
      const errorMessage = { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try asking your question again.' 
      };
      setMessages([...updatedMessages, errorMessage]);
    } finally {
      setIsLoading(false);
      // Refocus input for next question
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  };

  /**
   * Handle input change
   */
  const handleInputChange = (e) => {
    setCurrentInput(e.target.value);
  };

  /**
   * Handle Enter key press for submission
   */
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  /**
   * Clear conversation history
   */
  const clearHistory = () => {
    setMessages([]);
    setError(null);
    inputRef.current?.focus();
  };

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Page Header */}
      <div className="bg-white shadow-sm border-b border-gray-200 p-4">
        <div className="flex justify-between items-center max-w-4xl mx-auto">
          <div className="flex items-center space-x-3">
            <Link 
              to="/" 
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors flex items-center justify-center"
              title="Back to Homepage"
            >
              <ArrowLeft className="h-5 w-5 text-gray-600" />
            </Link>
            <h1 className="text-xl font-bold text-gray-800">
              {useRAG ? '🚀 RAG-Enhanced AI Assistant' : 'AI Assistant'}
            </h1>
            <div className="flex items-center space-x-2">
              <label className="flex items-center space-x-1 text-sm">
                <input
                  type="checkbox"
                  checked={useRAG}
                  onChange={(e) => setUseRAG(e.target.checked)}
                  className="rounded"
                />
                <span>Enhanced RAG Mode</span>
              </label>
            </div>
          </div>
          {messages.length > 0 && (
            <button
              onClick={clearHistory}
              className="px-4 py-2 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={isLoading}
            >
              Clear History
            </button>
          )}
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 max-w-4xl mx-auto w-full">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <div className="text-lg mb-2">
              👋 Welcome to U/C AI Assistant! {useRAG && '🚀'}
            </div>
            <p className="mb-4">
              {useRAG 
                ? "Ask me anything about machines, undercarriage components, maintenance schedules, or technical documentation. I have access to real-time data and uploaded documents."
                : "Ask me anything related and I'll help you based on uploaded documents and our conversation history."
              }
            </p>
            
            {useRAG && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left max-w-2xl mx-auto">
                <h3 className="font-semibold text-blue-800 mb-2">💡 Try these enhanced queries:</h3>
                <div className="text-sm text-blue-700 space-y-1">
                  <div>• "What machines need maintenance this week?"</div>
                  <div>• "Show me undercarriage components with low life remaining"</div>
                  <div>• "Which excavators have the highest operating hours?"</div>
                  <div>• "Calculate replacement costs for worn UC components"</div>
                  <div>• "Create a maintenance priority report"</div>
                </div>
              </div>
            )}
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl break-words ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white rounded-br-sm'
                    : 'bg-white border border-gray-200 text-gray-800 rounded-bl-sm shadow-sm'
                }`}
              >
                {/* Message role indicator for screen readers */}
                <span className="sr-only">
                  {message.role === 'user' ? 'You said:' : 'Assistant replied:'}
                </span>
                
                {/* Message content */}
                <div className="whitespace-pre-wrap">{message.content}</div>
                
                {/* Context info for RAG responses */}
                {message.contextInfo && useRAG && (
                  <div className="mt-2 p-2 bg-gray-50 border border-gray-200 rounded text-xs">
                    <div className="font-medium text-gray-700 mb-1">📊 Data Sources Used:</div>
                    <div className="text-gray-600">
                      {message.contextInfo.sql_sources && (
                        <div>
                          • Machine Records: {message.contextInfo.sql_sources.machine_records}
                          • UC Components: {message.contextInfo.sql_sources.uc_records}
                        </div>
                      )}
                      {message.contextInfo.pdf_sources > 0 && (
                        <div>• Documents: {message.contextInfo.pdf_sources}</div>
                      )}
                    </div>
                  </div>
                )}
                
                {/* Message metadata */}
                <div className={`text-xs mt-2 ${
                  message.role === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                  {message.role === 'user' ? 'You' : (useRAG && message.contextInfo ? 'RAG Assistant' : 'Assistant')}
                </div>
              </div>
            </div>
          ))
        )}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-sm shadow-sm px-4 py-3 max-w-xs">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
                <span className="text-sm text-gray-500">Assistant is typing...</span>
              </div>
            </div>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            <div className="flex items-center">
              <span className="text-red-500 mr-2">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
            {/* Input Section */}
      <div className="bg-white border-t border-gray-200 p-4">
        <div className="max-w-4xl mx-auto">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <div className="flex-1">
            <textarea
              ref={inputRef}
              value={currentInput}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="Ask me anything..."
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
              rows={1}
              disabled={isLoading}
              style={{ minHeight: '50px', maxHeight: '120px' }}
              onInput={(e) => {
                // Auto-resize textarea
                e.target.style.height = 'auto';
                e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
              }}
            />
          </div>
          <button
            type="submit"
            disabled={!currentInput.trim() || isLoading}
            className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              'Send'
            )}
          </button>
        </form>
        
        {/* Input hint */}
        <div className="text-xs text-gray-500 mt-2 px-1">
          Press Enter to send, Shift+Enter for new line
        </div>
        </div>
      </div>
    </div>
  );
};

export default ChatAsk;