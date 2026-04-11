<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="2.0"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9">
  <xsl:output method="html" version="1.0" encoding="UTF-8" indent="yes"/>
  <xsl:template match="/">
    <html>
      <head><title>Sitemap - accountability.ai</title></head>
      <body>
        <h1>XML Sitemap</h1>
        <table border="1" cellpadding="5">
          <tr><th>URL</th><th>Last Modified</th><th>Priority</th></tr>
          <xsl:for-each select="sitemap:urlset/sitemap:url">
            <tr>
              <td><xsl:value-of select="sitemap:loc"/></td>
              <td><xsl:value-of select="sitemap:lastmod"/></td>
              <td><xsl:value-of select="sitemap:priority"/></td>
            </tr>
          </xsl:for-each>
        </table>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>

