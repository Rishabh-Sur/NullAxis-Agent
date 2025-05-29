import React, { useState, useEffect, useRef} from 'react';
import './Index.css';

const Index = () => {
  const [email, setEmail] = useState('');
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [displayedResponse, setDisplayedResponse] = useState('');
  const [error, setError] = useState('');
  const [isTyping, setIsTyping] = useState(false);

  const validateEmail = (email) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

  const indexRef = useRef(0);

  useEffect(() => {
    if (response) {
      setIsTyping(true);
      setDisplayedResponse('');
      indexRef.current = 0;

      const timer = setInterval(() => {
        if (indexRef.current < response.length) {
          setDisplayedResponse(response.slice(0, indexRef.current + 1));
          indexRef.current += 1;
        } else {
          setIsTyping(false);
          clearInterval(timer);
        }
      }, 30);

      return () => clearInterval(timer);
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateEmail(email)) {
      setError('Please enter a valid email address.');
      return;
    }
    if (!query.trim()) {
      setError('Query cannot be empty.');
      return;
    }

    setError('');
    setResponse('');
    setDisplayedResponse('');

    try {
      // Replace this with your actual API call
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, message: query }),
      });
      const data = await res.json();
      setResponse(data.response);
      setQuery('');
    } catch (err) {
      setResponse('Error communicating with the server.');
    }
  };

  return (
    <div className="container">
      <div className="background-orbs"></div>
      <div className="main">
        <h1 className="title">NullAxis Agent</h1>
        <p className="subtitle">Your intelligent customer support assistant powered by advanced AI</p>
        <form className="form" onSubmit={handleSubmit}>
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Enter your email"
            required
          />
          <label>Message</label>
          <div className="query-wrapper">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask me anything..."
              required
            />
            <button type="submit" className="send-btn">➤</button>
          </div>
          {error && <div className="error">{error}</div>}
        </form>
        {displayedResponse && (
          <div className="response-box">
            <strong>Response:</strong>
            <p>
              {displayedResponse}
              {isTyping && <span className="cursor">|</span>}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Index;
