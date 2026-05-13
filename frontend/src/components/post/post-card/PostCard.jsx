import { useNavigate } from 'react-router-dom';
import { 
  HiOutlineLocationMarker, HiOutlineHeart, HiHeart, 
  HiOutlineChatAlt, HiOutlineTrash 
} from "react-icons/hi";
import { Avatar } from "@components/ui/avatar";
import styles from './PostCard.module.css';

export const PostCard = ({ post, onDelete, onLike, isOwn }) => {
  const navigate = useNavigate();
  const { 
    id, author, animal, tags, location, imageUrl, 
    title, content, createdAt, likesCount, isLiked, commentsCount 
  } = post;

  const handleCardClick = () => {
    navigate(`/post/${id}`);
  };

  const handleAuthorClick = (e) => {
    e.stopPropagation();
    e.preventDefault();
    if (author?.id) {
      navigate(`/profile/${author.id}`);
    }
  };

  const handleAction = (e, callback) => {
    e.stopPropagation();
    callback(id);
  };

  return (
    <article className={styles.postCard} onClick={handleCardClick}>
      {imageUrl ? (
        <div className={styles.imageContainer}>
          <img src={imageUrl} alt={title} className={styles.postImage} />
        </div>
      ) : (
        <div className={styles.imagePlaceholder}>Нет фото</div>
      )}

      <div className={styles.cardBody}>
        <div className={styles.authorSection} onClick={handleAuthorClick}>
          <Avatar user={author} size={36} />
          <div className={styles.authorInfo}>
            <span className={styles.authorName}>
              {author?.username || 'Инкогнито'}
            </span>
            <span className={styles.postDate}>
              {createdAt ? new Date(createdAt).toLocaleDateString('ru') : 'Недавно'}
            </span>
          </div>
        </div>

        <div className={styles.postContent}>
          <h3 className={styles.postTitle}>{title}</h3>
          
          {animal && (
            <div className={styles.animalTag}>
              <i className={styles.scientificName}>{animal.scientificName}</i>
            </div>
          )}
          
          <p className={styles.postDescription}>{content}</p>

          <div className={styles.hashtags}>
            {tags?.map((tag, idx) => (
              <span key={idx} className={styles.hashtag}>
                #{typeof tag === 'string' ? tag : tag.name}
              </span>
            ))}
          </div>

          {location && (
            <div className={styles.location}>
              <HiOutlineLocationMarker /> {location}
            </div>
          )}

          <div className={styles.postStats}>
            <div className={styles.statGroup}>
              <div
                className={`${styles.statItem} ${isLiked ? styles.liked : ''}`}
                onClick={(e) => handleAction(e, onLike)}
              >
                {isLiked ? <HiHeart /> : <HiOutlineHeart />} 
                <span>{likesCount ?? 0}</span>
              </div>
              
              <div className={styles.statItem}>
                <HiOutlineChatAlt /> 
                <span>{commentsCount ?? 0}</span>
              </div>
            </div>

            {isOwn && (
              <HiOutlineTrash
                className={styles.deleteBtn}
                onClick={(e) => handleAction(e, onDelete)}
              />
            )}
          </div>
        </div>
      </div>
    </article>
  );
};