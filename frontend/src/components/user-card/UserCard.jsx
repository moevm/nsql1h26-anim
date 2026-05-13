import { useNavigate } from 'react-router-dom';
import { Avatar } from '@components/ui/avatar';
import styles from './UserCard.module.css';

export const UserCard = ({ user, isOwn, onFollow, followLoading }) => {
  const navigate = useNavigate();

  return (
    <div className={styles.card} onClick={() => navigate(`/profile/${user.id}`)}>
      <Avatar user={user} size={50} />
      
      <div className={styles.info}>
        <div className={styles.nameRow}>
          <span className={styles.fullName}>
            {user.firstName} {user.lastName}
          </span>
          <span className={styles.username}>@{user.username}</span>
        </div>
        {user.bio && <p className={styles.bio}>{user.bio}</p>}
      </div>

      {!isOwn && (
        <button
          className={user.isFollowed ? styles.unfollowBtn : styles.followBtn}
          disabled={followLoading}
          onClick={(e) => {
            e.stopPropagation();
            onFollow(user.id);
          }}
        >
          {user.isFollowed ? 'Вы подписаны' : 'Подписаться'}
        </button>
      )}
    </div>
  );
};