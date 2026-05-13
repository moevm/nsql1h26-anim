import { useState } from 'react';
import { HiOutlinePaperAirplane, HiOutlineX } from "react-icons/hi";
import { request } from "@api/axios";
import { Avatar } from "@components/ui/avatar";
import styles from './ReplyForm.module.css';

export const ReplyForm = ({ parentId, postId, currentAuthor, onSubmitted, onCancel }) => {
  const [text, setText] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return;
    setSubmitting(true);
    try {
      const created = await request('POST', 'comments', {
        content: text.trim(),
        targetId: postId,
        parentId,
      });
      onSubmitted(created);
      setText('');
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className={styles.replyForm}>
      <Avatar user={currentAuthor} size={28} />
      <input
        className={styles.replyInput}
        placeholder="Ваш ответ..."
        value={text}
        autoFocus
        onChange={e => setText(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSubmit()}
      />
      <div className={styles.replyActions}>
        <button
          className={styles.replySubmit}
          onClick={handleSubmit}
          disabled={submitting || !text.trim()}
        >
          <HiOutlinePaperAirplane className={styles.sendIcon} />
        </button>
        <button className={styles.replyCancel} onClick={onCancel}>
          <HiOutlineX />
        </button>
      </div>
    </div>
  );
};