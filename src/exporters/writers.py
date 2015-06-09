def TextWriter(topics, queryScore, fname):
    with open(fname, "w") as f:
        f.write("\n".join(["Topic " + str(i) + " : " + " ".join([w[1] for w in topics[i]]) for i in range(len(topics))]))
        f.write("\n\n")

        # f.write("\n".join(["Topic " + " ".join([w[1] for w in words]) for words in queryScore]))
        f.close

def TopWordsWriter(legend, words, query=[], markdown=False, fname="topwords.txt"):
    data = legend + words + query
    if markdown is True:
      with open(fname, "w") as f:
        f.write(
          "\n".join(
              [ " | ".join([str(e) for e in list(r)]) for r in data]
            )
        )
        f.close()
    else:
      with open(fname, "w") as f:
        f.write(
          "\n".join(
              [ " ; ".join([str(e) for e in list(r)]) for r in data]
            )
        )
        f.close()
