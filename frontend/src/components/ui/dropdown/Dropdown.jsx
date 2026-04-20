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
  
  const handleClick = () => {
    setIsOpen(!isOpen)
  }

  return (
    <div className={styles['dropdown']} ref={dropdownRef}>
      <button 
        className={styles['dropdown-button']}
        onClick={handleClick}
      >
        {trigger} 
        {isOpen ? <RiArrowDropDownLine size={20}/> : <RiArrowDropUpLine size={20}/>}
      </button>
      {isOpen && (
        <div className={`
          ${styles['dropdown-menu']} 
          ${styles[`dropdown-menu-${position}`]}
        `}>
          {items.map((item, index) => {
            if (item.onClick) {
              return (
                <div 
                  key={index} 
                  className={styles['dropdown-menu-item']}
                  onClick={() => {
                    item.onClick();
                    setIsOpen(false);
                  }}
                  style={{ cursor: 'pointer' }}
                >
                  {item.icon && <div className={styles['item-icon']}>{item.icon}</div>}
                  <span className={styles['item-label']}>{item.label}</span>
                </div>
              )
            }

            return (
              <Link 
                to={item.to} 
                key={index} 
                className={styles['dropdown-menu-item']}
                onClick={() =>  setIsOpen(false)}
              >
                {item.icon && <div className={styles['item-icon']}>{item.icon}</div>}
                <span className={styles['item-label']}>{item.label}</span>
              </Link>
            )
          })}
        </div>
      )}
    </div>
  );
}