export interface ParsedExpense {
  date: string;  // YYYY-MM-DD format
  vendor: string;
  price: number;
}

export function parseExpectedExpenses(text: string): ParsedExpense[] {
  const expenses: ParsedExpense[] = [];

  for (const line of text.trim().split('\n')) {
    const trimmedLine = line.trim();
    if (!trimmedLine) continue;

    const parts = trimmedLine.split('-').map(p => p.trim());
    if (parts.length !== 3) continue;

    const [dateStr, part1, part2] = parts;

    // Parse date (MM/DD/YY format)
    try {
      const [month, day, year] = dateStr.split('/');
      const fullYear = parseInt(year) >= 50 ? `19${year}` : `20${year}`;
      const isoDate = `${fullYear}-${month.padStart(2, '0')}-${day.padStart(2, '0')}`;

      // Determine which part is price and which is vendor
      let price: number;
      let vendor: string;

      if (part1.startsWith('$')) {
        price = parseFloat(part1.replace('$', '').replace(',', ''));
        vendor = part2;
      } else {
        vendor = part1;
        price = parseFloat(part2.replace('$', '').replace(',', ''));
      }

      if (isNaN(price)) continue;

      expenses.push({ date: isoDate, vendor, price });
    } catch {
      continue;
    }
  }

  return expenses;
}
