interface InlineErrorProps {
  message: string;
  id?: string;
}

/** Small inline validation error shown below form fields */
export function InlineError({ message, id }: InlineErrorProps) {
  return (
    <p
      id={id}
      role="alert"
      aria-live="polite"
      className="text-xs text-red-600 dark:text-red-400 mt-1"
    >
      {message}
    </p>
  );
}
