import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '@contexts/index';
import { Header } from "@components/header";
import { Avatar } from "@components/ui/avatar";
import { CommentItem } from "@components/comment";
import { PostModal } from "@components/post";
import { request } from "@api/axios";
import {
  HiOutlineArrowLeft, HiOutlineHeart, HiHeart,
  HiOutlineChatAlt, HiOutlineTrash, HiOutlinePaperAirplane,
  HiOutlinePencilAlt
} from "react-icons/hi";
import styles from './PostDetailPage.module.css';

export const PostDetailPage = () => {
  const { user: currentUser } = useAuth()
  const { postId } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [fetching, setFetching] = useState(true);
  const [newComment, setNewComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [editLoading, setEditLoading] = useState(false);

  const fetchData = useCallback(async () => {
    setFetching(true);
    try {
      const data = await request('GET', `posts/${postId}`);
      setPost(data);
      setComments(Array.isArray(data?.comments) ? data.comments : []);
    } catch (err) {
      console.error("Ошибка загрузки поста:", err);
    } finally {
      setFetching(false);
    }
  }, [postId]);

  useEffect(() => { fetchData(); }, [fetchData]);

  const handlePostLike = async () => {
    if (!post) return;
    const wasLiked = post.isLiked;
    setPost(prev => ({
      ...prev,
      isLiked: !wasLiked,
      likesCount: wasLiked ? prev.likesCount - 1 : prev.likesCount + 1
    }));
    try {
      await request('POST', `posts/${postId}/like`);
    } catch {
      fetchData();
    }
  };

  const handlePostDelete = async () => {
    if (!window.confirm('Вы уверены, что хотите удалить этот пост?')) return;
    try {
      await request('DELETE', `posts/${postId}`);
      navigate('/feed');
    } catch (err) {
      alert("Не удалось удалить пост: " + err);
    }
  };

  const handleEdit = async (payload) => {
    setEditLoading(true);
    try {
      const updated = await request('PATCH', `posts/${postId}`, payload);
      setPost(prev => ({ ...prev, ...updated }));
      setEditOpen(false);
    } catch (err) {
      alert("Ошибка редактирования: " + err);
    } finally {
      setEditLoading(false);
    }
  };

  const handleCommentSubmit = async () => {
    if (!newComment.trim()) return;
    setSubmitting(true);
    try {
      const created = await request('POST', 'comments/', {
        content: newComment.trim(),
        targetId: postId,
        parentId: null
      });
      setComments(prev => [created, ...prev]);
      setPost(prev => ({ ...prev, commentsCount: (prev.commentsCount ?? 0) + 1 }));
      setNewComment('');
    } catch (err) {
      console.error("Ошибка создания комментария:", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleCommentEdit = (id, newContent) => {
    const update = c => c.id === id ? { ...c, content: newContent } : c;
    setComments(prev => prev.map(c => ({
      ...update(c),
      replies: (c.replies ?? []).map(update)
    })));
  };

  const handleReplySubmitted = (parentId, created) => {
    setComments(prev => prev.map(c =>
      c.id === parentId
        ? { ...c, replies: [...(c.replies ?? []), created] }
        : c
    ));
    setPost(prev => ({ ...prev, commentsCount: (prev.commentsCount ?? 0) + 1 }));
  };

  const handleCommentDelete = async (id) => {
    if (!window.confirm('Удалить комментарий?')) return;
    try {
      await request('DELETE', `comments/${id}`);
      let removedCount = 0;
      setComments(prev => {
        const target = prev.find(c => c.id === id);
        if (target) {
          removedCount = 1 + (target.replies?.length ?? 0);
          return prev.filter(c => c.id !== id);
        } else {
          removedCount = 1;
          return prev.map(c => ({
            ...c,
            replies: (c.replies ?? []).filter(r => r.id !== id)
          }));
        }
      });
      setPost(prev => ({
        ...prev,
        commentsCount: Math.max(0, (prev.commentsCount ?? 0) - removedCount)
      }));
    } catch (err) {
      alert("Ошибка при удалении комментария: " + err);
    }
  };

  const handleCommentLike = async (id) => {
    const toggle = c => c.id === id
      ? { ...c, isLiked: !c.isLiked, likesCount: c.isLiked ? c.likesCount - 1 : c.likesCount + 1 }
      : c;
    setComments(prev => prev.map(c => ({
      ...toggle(c),
      replies: (c.replies ?? []).map(toggle)
    })));
    try {
      await request('POST', `comments/${id}/like`);
    } catch {
      fetchData();
    }
  };

  if (fetching) return <div className={styles.loading}>Загрузка...</div>;
  if (!post) return <div className={styles.loading}>Пост не найден</div>;

  return (
    <div className={styles.wrapper}>
      <Header />
      <main className={styles.main}>
        <button className={styles.backBtn} onClick={() => navigate(-1)}>
          <HiOutlineArrowLeft /> Назад
        </button>

        <article className={styles.card}>
          {post.imageUrl && (
            <div className={styles.imageWrap}>
              <img src={post.imageUrl} alt={post.title} className={styles.image} />
            </div>
          )}
          <div className={styles.cardBody}>
            <div className={styles.titleRow}>
              <h1 className={styles.title}>{post.title}</h1>
              {currentUser?.id === post.author?.id && (
                <div className={styles.titleActions}>
                  <button className={styles.editBtn} onClick={() => setEditOpen(true)}>
                    <HiOutlinePencilAlt />
                  </button>
                  <button className={styles.deleteBtn} onClick={handlePostDelete}>
                    <HiOutlineTrash />
                  </button>
                </div>
              )}
            </div>

            {post.animal && (
              <div className={styles.animalTag}>
                <strong>{post.animal.name}</strong>
                <i className={styles.scientificName}>{post.animal.scientificName}</i>
              </div>
            )}

            <div className={styles.authorRow}>
              <Avatar user={post.author} size={40} />
              <div className={styles.authorMeta}>
                <span className={styles.authorName}>@{post.author?.username}</span>
                <span className={styles.postDate}>
                  {new Date(post.createdAt).toLocaleDateString()}
                </span>
              </div>
            </div>

            <p className={styles.content}>{post.content}</p>

            <div className={styles.stats}>
              <button
                className={`${styles.statBtn} ${post.isLiked ? styles.statLiked : ''}`}
                onClick={handlePostLike}
              >
                {post.isLiked ? <HiHeart /> : <HiOutlineHeart />}
                <span>{post.likesCount}</span>
              </button>
              <div className={styles.statBtn}>
                <HiOutlineChatAlt />
                <span>{post.commentsCount}</span>
              </div>
            </div>
          </div>
        </article>

        <section className={styles.commentsSection}>
          <h2 className={styles.commentsTitle}>Комментарии ({post.commentsCount})</h2>
          <div className={styles.commentForm}>
            <input
              className={styles.commentInput}
              placeholder="Оставьте ваш комментарий..."
              value={newComment}
              onChange={e => setNewComment(e.target.value)}
              onKeyDown={e => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleCommentSubmit();
                }
              }}
            />
            <button
              className={styles.commentSubmit}
              onClick={handleCommentSubmit}
              disabled={submitting || !newComment.trim()}
            >
              <HiOutlinePaperAirplane className={styles.sendIcon} />
            </button>
          </div>

          <div className={styles.commentsList}>
            {comments.length > 0 ? (
              comments.map(c => (
                <CommentItem
                  key={c.id}
                  comment={c}
                  postId={postId}
                  currentAuthor={currentUser}
                  onDelete={handleCommentDelete}
                  onLike={handleCommentLike}
                  onEdit={handleCommentEdit}
                  onReplySubmitted={handleReplySubmitted}
                />
              ))
            ) : (
              <p className={styles.noComments}>Здесь пока нет комментариев</p>
            )}
          </div>
        </section>
      </main>

      <PostModal
        isOpen={editOpen}
        onClose={() => setEditOpen(false)}
        onSubmit={handleEdit}
        loading={editLoading}
        post={post}
      />
    </div>
  );
};