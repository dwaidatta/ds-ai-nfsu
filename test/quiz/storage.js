// Shared client-side "cloud save" for the quiz feature.
// Everything lives in this browser's localStorage under the `dsaiQuiz:` prefix —
// there is no server, so progress and history do not sync across devices/browsers.
const QuizStorage = (() => {
  const PROGRESS_PREFIX = 'dsaiQuiz:progress:';
  const HISTORY_KEY = 'dsaiQuiz:history';

  function safeGet(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }

  function safeSet(key, value) {
    try { localStorage.setItem(key, value); return true; } catch (e) { return false; }
  }

  function safeRemove(key) {
    try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
  }

  function getProgress(quizId) {
    const raw = safeGet(PROGRESS_PREFIX + quizId);
    if (!raw) return null;
    try { return JSON.parse(raw); } catch (e) { return null; }
  }

  function saveProgress(quizId, answers) {
    safeSet(PROGRESS_PREFIX + quizId, JSON.stringify({ answers, updatedAt: new Date().toISOString() }));
  }

  function clearProgress(quizId) {
    safeRemove(PROGRESS_PREFIX + quizId);
  }

  function getHistory() {
    const raw = safeGet(HISTORY_KEY);
    if (!raw) return [];
    try {
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function addHistoryEntry(entry) {
    const history = getHistory();
    history.push(entry);
    safeSet(HISTORY_KEY, JSON.stringify(history));
    return history;
  }

  function clearAll() {
    try {
      Object.keys(localStorage)
        .filter((k) => k.startsWith('dsaiQuiz:'))
        .forEach((k) => localStorage.removeItem(k));
    } catch (e) { /* ignore */ }
  }

  return { getProgress, saveProgress, clearProgress, getHistory, addHistoryEntry, clearAll };
})();
