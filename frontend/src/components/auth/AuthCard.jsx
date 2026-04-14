const cardStyle = {
  display: 'flex',
  alignItems: 'center',
  flexDirection: 'column',
  width: '100%',
  gap: '16px',
  padding: '40px 20px',
  backgroundColor: '#fff',
  borderRadius: '8px',
  boxShadow: '0px 0px 8px rgba(0, 0, 0, 0.25)'
}

export const AuthCard = ({
  children,
  className
}) => {
  return (
    <div style ={cardStyle} className={className}>
      {children}
    </div>
  );
}