"use client";

interface DataTableProps<TData> {
  columns: { header: string; accessorKey: keyof TData }[];
  data: TData[];
}

export function DataTable<TData>({ columns, data }: DataTableProps<TData>) {
  return (
    <div className="rounded-md border border-border/50 overflow-hidden">
      <table className="w-full text-sm">
        <thead className="border-b bg-muted/50 text-muted-foreground">
          <tr>
            {columns.map((col, i) => (
              <th
                key={i}
                className="h-10 px-4 text-left align-middle font-medium"
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-border/50">
          {data.length > 0 ? (
            data.map((row, rowIndex) => (
              <tr
                key={rowIndex}
                className="hover:bg-muted/30 data-[state=selected]:bg-muted transition-colors"
              >
                {columns.map((col, colIndex) => (
                  <td key={colIndex} className="p-4 align-middle">
                    {String(row[col.accessorKey])}
                  </td>
                ))}
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={columns.length} className="h-24 text-center">
                No results.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
