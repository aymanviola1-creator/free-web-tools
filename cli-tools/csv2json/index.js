#!/usr/bin/env node

/**
 * csv2json — Convert CSV files to JSON
 *
 * Usage:
 *   node index.js <input.csv> [output.json]
 *   node index.js <input.csv> --pretty
 *   node index.js <input.csv> --ndjson
 *   cat data.csv | node index.js
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

// ── Parse CSV line with proper quote handling ──
function parseCSVLine(line) {
  const result = [];
  let current = '';
  let inQuotes = false;

  for (let i = 0; i < line.length; i++) {
    const char = line[i];
    const next = line[i + 1];

    if (inQuotes) {
      if (char === '"') {
        if (next === '"') {
          current += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        current += char;
      }
    } else {
      if (char === '"') {
        inQuotes = true;
      } else if (char === ',') {
        result.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
  }
  result.push(current.trim());
  return result;
}

// ── Infer type from string value ──
function inferType(value) {
  if (value === '' || value === undefined || value === null) return null;
  if (value.toLowerCase() === 'true') return true;
  if (value.toLowerCase() === 'false') return false;
  if (value.toLowerCase() === 'null' || value.toLowerCase() === 'nil') return null;

  // Number
  const num = Number(value);
  if (!isNaN(num) && value.trim() !== '') return num;

  return value;
}

// ── Convert CSV rows to JSON objects ──
function csvToJSON(headers, rows) {
  return rows.map(row => {
    const obj = {};
    headers.forEach((header, index) => {
      const value = row[index] || '';
      obj[header.trim()] = inferType(value);
    });
    return obj;
  });
}

// ── Main converter ──
async function convert(inputPath, outputPath, options = {}) {
  const { pretty = false, ndjson = false, noType = false } = options;
  const inputStream = inputPath
    ? fs.createReadStream(inputPath, 'utf-8')
    : process.stdin;

  const rl = readline.createInterface({ input: inputStream, crlfDelay: Infinity });

  let headers = null;
  const rows = [];
  let lineCount = 0;

  for await (const rawLine of rl) {
    const line = rawLine.trim();
    if (!line) continue; // Skip empty lines

    lineCount++;

    if (!headers) {
      headers = parseCSVLine(line);
      continue;
    }

    const values = parseCSVLine(line);
    rows.push(values);
  }

  if (!headers) {
    console.error('❌ Error: No headers found in CSV.');
    process.exit(1);
  }

  const result = csvToJSON(headers, rows);

  // Output
  let output;
  if (ndjson) {
    output = result.map(r => JSON.stringify(r)).join('\n');
  } else if (pretty) {
    output = JSON.stringify(result, null, 2);
  } else {
    output = JSON.stringify(result);
  }

  if (outputPath) {
    fs.writeFileSync(outputPath, output, 'utf-8');
    console.log(`✅ Converted ${result.length} rows from "${path.basename(inputPath)}" → "${path.basename(outputPath)}"`);
    console.log(`   Lines: ${lineCount - 1} data rows, ${headers.length} columns`);
    if (ndjson) console.log('   Format: NDJSON');
    else if (pretty) console.log('   Format: Pretty JSON');
  } else {
    console.log(output);
  }

  return { rows: result.length, columns: headers.length };
}

// ── CLI ──
async function main() {
  const args = process.argv.slice(2);
  const options = { pretty: false, ndjson: false, noType: false };

  // Parse flags
  const positional = args.filter(a => {
    if (a === '--pretty' || a === '-p') { options.pretty = true; return false; }
    if (a === '--ndjson' || a === '-n') { options.ndjson = true; return false; }
    if (a === '--no-type' || a === '-t') { options.noType = true; return false; }
    if (a === '--help' || a === '-h') { showHelp(); process.exit(0); }
    return true;
  });

  const inputPath = positional[0];
  const outputPath = positional[1];

  // Validate input file exists
  if (inputPath && !fs.existsSync(inputPath)) {
    console.error(`❌ Error: File "${inputPath}" not found.`);
    process.exit(1);
  }

  // Validate extension
  if (inputPath && !inputPath.toLowerCase().endsWith('.csv')) {
    console.error(`⚠️  Warning: Input file doesn't have a .csv extension. Proceeding anyway.`);
  }

  // Validate output extension
  if (outputPath && !outputPath.toLowerCase().endsWith('.json')) {
    console.error(`⚠️  Warning: Output file doesn't have a .json extension. Proceeding anyway.`);
  }

  try {
    await convert(inputPath, outputPath, options);
  } catch (err) {
    console.error(`❌ Error: ${err.message}`);
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
csv2json — Convert CSV files to JSON

USAGE:
  csv2json <input.csv> [output.json]   Convert CSV to JSON
  csv2json <input.csv> --pretty         Pretty-print output
  csv2json <input.csv> --ndjson         Output as NDJSON (one JSON object per line)
  cat data.csv | csv2json               Read from stdin
  csv2json --help                       Show this help

OPTIONS:
  -p, --pretty      Pretty-print JSON output
  -n, --ndjson      Output as NDJSON (newline-delimited JSON)
  -t, --no-type     Disable automatic type inference (keep all values as strings)
  -h, --help        Show this help message

EXAMPLES:
  csv2json data.csv output.json
  csv2json data.csv --pretty
  csv2json data.csv --ndjson > output.ndjson
  cat data.csv | csv2json --pretty
`);
}

if (require.main === module) {
  main();
}

module.exports = { convert, parseCSVLine, csvToJSON, inferType };
