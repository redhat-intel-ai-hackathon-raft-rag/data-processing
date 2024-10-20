LOAD CSV FROM "file:///path/to/your/data.json" AS line
WITH line, jsonExtract(line.data, '$.array') AS array_data
FOREACH (item IN array_data |
  CREATE (node:Node {property1: item.property1, property2: item.property2})
);
