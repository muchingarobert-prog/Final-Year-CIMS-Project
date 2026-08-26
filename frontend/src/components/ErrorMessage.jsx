export default function ErrorMessage({ message, variant = 'error' }) {
  return (
    <div className={variant === 'success' ? 'success-message' : 'error-message'}>
      {message}
    </div>
  );
}
