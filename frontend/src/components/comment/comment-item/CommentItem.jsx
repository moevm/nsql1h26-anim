import { useState } from 'react';
import { Link } from 'react-router-dom';
import { HiOutlineTrash, HiHeart, HiOutlineHeart, HiOutlineReply, HiOutlinePencilAlt, HiOutlineX, HiOutlineCheck } from "react-icons/hi";
import { Avatar } from "@components/ui/avatar";
import { ReplyForm } from "../reply-form/ReplyForm";
import { request } from '@api/axios';
import styles from './CommentItem.module.css';

export const CommentItem = ({ 
  comment, postId, currentAuthor, onDelete, onLike, onReplySubmitted, onEdit, depth = 0 
}) => {
  const [replyOpen, setReplyOpen] = useState(false);
  const [editing, setEditing] = useState(false);
  const [editValue, setEditValue] = useState(comment.content);
  const [editLoading, setEditLoading] = useState(false);

  const isOwn = currentAuthor?.id === comment.author?.id;
  const profilePath = comment.author?.id ? `/profile/${comment.author.id}` : '#';

  const handleReplySuccess = (created) => {
    onReplySubmitted(comment.id, created);
    setReplyOpen(false);
  };

  const handleEditSubmit = async () => {
    if (!editValue.trim() || editValue === comment.content) {
      setEditing(false);
      return;
    }
    setEditLoading(true);
    try {
      const updated = await request('PATCH', `comments/${comment.id}`, { content: editValue.trim() });
      onEdit(comment.id, updated.content);
      setEditing(false);
    } catch (err) {
      console.error("Ошибка редактирования:", err);
    } finally {
      setEditLoading(false);
    }
  };

  const handleEditCancel = () => {
    setEditValue(comment.content);
    setEditing(false);
  };

  return (
    <div className={`${styles.commentItem} ${depth > 0 ? styles.commentReply : ''}`}>
      <Link to={profilePath} className={styles.avatarLink}>
        <Avatar user={comment.author} size={depth > 0 ? 28 : 36} />
      </Link>

      <div className={styles.commentBody}>
        <div className={styles.commentHeader}>
          <Link to={profilePath} className={styles.authorNameLink}>
            <span className={styles.commentAuthor}>@{comment.author?.username}</span>
          </Link>

          <div className={styles.commentMeta}>
            <span className={styles.commentDate}>
              {comment.createdAt && new Date(comment.createdAt).toLocaleString('ru', {
                day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
              })}
            </span>

            {isOwn && !editing && (
              <>
                <HiOutlinePencilAlt
                  className={styles.commentEdit}
                  onClick={() => setEditing(true)}
                />
                <HiOutlineTrash
                  className={styles.commentDelete}
                  onClick={() => onDelete(comment.id)}
                />
              </>
            )}
          </div>
        </div>

        {editing ? (
          <div className={styles.editForm}>
            <input
              className={styles.editInput}
              value={editValue}
              onChange={e => setEditValue(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleEditSubmit(); }
                if (e.key === 'Escape') handleEditCancel();
              }}
              autoFocus
              disabled={editLoading}
            />
            <div className={styles.editActions}>
              <button className={styles.editConfirm} onClick={handleEditSubmit} disabled={editLoading}>
                <HiOutlineCheck />
              </button>
              <button className={styles.editCancelBtn} onClick={handleEditCancel}>
                <HiOutlineX />
              </button>
            </div>
          </div>
        ) : (
          <p className={styles.commentText}>{comment.content}</p>
        )}

        <div className={styles.commentActions}>
          <button
            className={`${styles.commentLike} ${comment.isLiked ? styles.commentLiked : ''}`}
            onClick={() => onLike(comment.id)}
          >
            {comment.isLiked ? <HiHeart /> : <HiOutlineHeart />}
            <span>{comment.likesCount ?? 0}</span>
          </button>

          {depth === 0 && (
            <button className={styles.replyBtn} onClick={() => setReplyOpen(!replyOpen)}>
              <HiOutlineReply />
              <span>Ответить</span>
            </button>
          )}
        </div>

        {replyOpen && (
          <div className={styles.replyFormWrapper}>
            <ReplyForm
              parentId={comment.id}
              postId={postId}
              currentAuthor={currentAuthor}
              onSubmitted={handleReplySuccess}
              onCancel={() => setReplyOpen(false)}
            />
          </div>
        )}

        {comment.replies?.length > 0 && (
          <div className={styles.repliesList}>
            {comment.replies.map(reply => (
              <CommentItem
                key={reply.id}
                comment={reply}
                postId={postId}
                currentAuthor={currentAuthor}
                onDelete={onDelete}
                onLike={onLike}
                onReplySubmitted={onReplySubmitted}
                onEdit={onEdit}
                depth={depth + 1}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};