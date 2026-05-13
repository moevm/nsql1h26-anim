import { 
    HiOutlineCalendar, 
    HiOutlinePencil, 
    HiOutlineCheck, 
    HiOutlineX, 
    HiOutlineUserAdd, 
    HiOutlineUserRemove, 
    HiOutlinePhotograph, 
    HiOutlineColorSwatch 
} from 'react-icons/hi';
import { Avatar } from '@components/ui/avatar';
import styles from './ProfileHeader.module.css';

export const ProfileHeader = ({ 
    isOwn, 
    editing, 
    user, 
    editForm, 
    setEditForm, 
    onSave, 
    onCancel, 
    onEdit, 
    onFollow, 
    followLoading 
}) => {
  return (
    <div className={styles.header}>
      <div className={styles.mainInfo}>
        <div className={styles.avatarBlock}>
          <Avatar user={editing ? { ...user, ...editForm } : user} size={120} />
          {editing && (
            <div className={styles.avatarEditControls}>
              <div className={styles.editField}>
                <label><HiOutlinePhotograph /> URL фото</label>
                <input 
                  value={editForm.avatarUrl} 
                  onChange={e => setEditForm(p => ({ ...p, avatarUrl: e.target.value }))}
                />
              </div>
              <div className={styles.editField}>
                <label><HiOutlineColorSwatch /> Фон</label>
                <input 
                  type="color"
                  value={editForm.avatarBackgroundColor} 
                  onChange={e => setEditForm(p => ({ ...p, avatarBackgroundColor: e.target.value }))}
                />
              </div>
            </div>
          )}
        </div>

        <div className={styles.textContent}>
          <h1 className={styles.username}>@{user.username}</h1>
          <div className={styles.meta}>
            <HiOutlineCalendar />
            <span>С {new Date(user.createdAt).toLocaleDateString('ru', { month: 'long', year: 'numeric' })}</span>
          </div>
          {user.bio && !editing && <p className={styles.bio}>{user.bio}</p>}
          {editing && (
            <textarea 
              className={styles.bioInput}
              value={editForm.bio}
              onChange={e => setEditForm(p => ({ ...p, bio: e.target.value }))}
              placeholder="Расскажите о себе..."
            />
          )}
        </div>
      </div>

      <div className={styles.actions}>
        {isOwn ? (
          editing ? (
            <div className={styles.btnGroup}>
              <button className={styles.btnSave} onClick={onSave}><HiOutlineCheck /> Сохранить</button>
              <button className={styles.btnCancel} onClick={onCancel}><HiOutlineX /></button>
            </div>
          ) : (
            <button className={styles.btnEdit} onClick={onEdit}><HiOutlinePencil /> Редактировать</button>
          )
        ) : (
          <button 
            className={user.isFollowed ? styles.btnUnfollow : styles.btnFollow} 
            onClick={onFollow}
            disabled={followLoading}
          >
            {user.isFollowed ? <><HiOutlineUserRemove /> Отписаться</> : <><HiOutlineUserAdd /> Подписаться</>}
          </button>
        )}
      </div>
    </div>
  );
};