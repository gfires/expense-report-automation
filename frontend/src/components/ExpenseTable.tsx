interface Column<T> {
  key: keyof T;
  label: string;
  formatter?: (value: unknown) => string;
}

interface ExpenseTableProps<T> {
  columns: Column<T>[];
  data: T[];
}

export default function ExpenseTable<T>({
  columns,
  data,
}: ExpenseTableProps<T>) {
  return (
    <div className="table-container">
      <table className="expense-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={String(col.key)}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((col) => (
                <td key={String(col.key)}>
                  {col.formatter
                    ? col.formatter(row[col.key])
                    : String(row[col.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
