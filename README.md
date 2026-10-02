# GA4GH Data Security Work Stream

This is the repository for the source of any specifications/documentation
of the Data Security Work Stream of the Global Alliance for Genomics and Health ([GA4GH](https://www.ga4gh.org/)).

## Resources

- [Data Security and Infrastructure Policy](DSIP/DSIP_v4.0.md)
- [Authentication and Authorization Infrastructure](AAI/README.md)


## Rendering documentation

The source is written in Markdown and processed via Jekyll. Diagrams make use of PlantUML.

To produce a local copy, clone the repository and run

```shell
make
```

or alternatively run the simple `docker` command shown in the Makefile (runs Jekyll in `serve` mode).

The local copy can then be browsed at

```text
http://localhost:4000/local/
```

(Assuming default port 4000). To use a different port, run e.g. `make PORT=4001`
and browse to `http://localhost:4001/local/` instead.

### Use of Jekyll

The following Liquid tags are used to separate

Second level headers - {% hr2 %} 

Third level headers - {% hr3 %}

Fourth level headers - {% hr4 %}

Note that level 5 and 6 headers render smaller than paragraph text and are not
distinctive - and therefore should be avoided.

Use **text** for a 5th level header if required.

The actual HTML for these dividers can be found in `_plugins/jekyll-hrs.rb`.
