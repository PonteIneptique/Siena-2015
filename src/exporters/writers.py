import json
def TextWriter(topics, queryScore, fname):
    with open(fname, "w") as f:
        f.write("\n".join(["Topic " + str(i) + " : " + " ".join([w[1] for w in topics[i]]) for i in range(len(topics))]))
        f.write("\n\n")

        # f.write("\n".join(["Topic " + " ".join([w[1] for w in words]) for words in queryScore]))
        f.close

def TopWordsWriter(legend, words, query=[], mode=False, fname="topwords.txt"):
    merged = legend + words + query
    if mode == "markdown":
      with open(fname, "w") as f:
        f.write(
          "\n".join(
              [ " | ".join([str(e) for e in list(r)]) for r in merged]
            )
        )
        f.close()
    elif mode == "json":
        data = words + query
        output = []
        for row in data:
            topics = list(row)[1:]
            output.append({
                "topic" : [
                    (i, topics[i])
                    for i
                    in range(len(topics))
                ],
                "name" : row.label
            })
        with open(fname, "w") as f:
            f.write(json.dumps(output))
            f.close()
    else:
      with open(fname, "w") as f:
        f.write(
          "\n".join(
              [ " ; ".join([str(e) for e in list(r)]) for r in merged]
            )
        )
        f.close()
