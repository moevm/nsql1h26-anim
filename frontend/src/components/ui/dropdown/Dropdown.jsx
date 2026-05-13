import { useState, useEffect, useRef } from 'react'
import { Link } from 'react-router-dom';
import { RiArrowDropDownLine, RiArrowDropUpLine } from "react-icons/ri";
import styles from './Dropdown.module.css'

export const Dropdown = ({
  trigger,
  items,
  position = 'bottom'
}) => {
  const [isOpen, setIsOpen] = useState(false)
  const dropdownRef = useRef(null)

  useEffect(() => {
    const handleClickOutsideMenu = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutsideMenu)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutsideMenu)
    }
  }, [isOpen])
  
  const toggleDropdown = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsOpen(prev => !prev);
  }

  return (
    <div className={styles.dropdown} ref={dropdownRef}>
      <div 
        className={styles['dropdown-trigger']} 
        onClick={toggleDropdown}
      >
        <div className={styles['trigger-content']}>
          {trigger}
        </div>
        <div className={styles['arrow-icon']}>
          {isOpen ? <RiArrowDropUpLine size={24}/> : <RiArrowDropDownLine size={24}/>}
        </div>
      </div>

      {isOpen && (
        <div className={`
          ${styles['dropdown-menu']} 
          ${styles[`dropdown-menu-${position}`]}
        `}>
          {items.map((item, index) => {
            const content = (
              <>
                {item.icon && <div className={styles['item-icon']}>{item.icon}</div>}
                <span className={styles['item-label']}>{item.label}</span>
              </>
            );

            if (item.onClick) {
              return (
                <div 
                  key={index} 
                  className={styles['dropdown-menu-item']}
                  onClick={(e) => {
                    e.stopPropagation();
                    item.onClick();
                    setIsOpen(false);
                  }}
                >
                  {content}
                </div>
              )
            }

            return (
              <Link 
                to={item.to} 
                key={index} 
                className={styles['dropdown-menu-item']}
                onClick={() => setIsOpen(false)}
              >
                {content}
              </Link>
            )
          })}
        </div>
      )}
    </div>
  );
}