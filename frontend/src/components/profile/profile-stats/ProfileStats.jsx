import { HiOutlineHeart, HiOutlineChatAlt, HiOutlineUserGroup } from 'react-icons/hi';
import { GiPaw } from 'react-icons/gi';
import styles from './ProfileStats.module.css';

export const ProfileStats = ({ user }) => {
  const stats = [
    { label: 'наблюдений', value: user.postsCount ?? 0, icon: <GiPaw />, color: '#386a51' },
    { label: 'лайков', value: user.likesCount ?? 0, icon: <HiOutlineHeart />, color: '#e11d48' },
    { label: 'комментов', value: user.commentsCount ?? 0, icon: <HiOutlineChatAlt />, color: '#2563eb' },
    { label: 'подписчиков', value: user.followersCount ?? 0, icon: <HiOutlineUserGroup />, color: '#7c3aed' },
  ];

  return (
    <div className={styles.container}>
      {stats.map(s => (
        <div key={s.label} className={styles.card}>
          <div className={styles.icon} style={{ color: s.color }}>{s.icon}</div>
          <div className={styles.data}>
            <span className={styles.value}>{s.value}</span>
            <span className={styles.label}>{s.label}</span>
          </div>
        </div>
      ))}
    </div>
  );
};