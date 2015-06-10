<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:excerpt="http://wordpress.org/export/1.2/excerpt/"
    xmlns:content="http://purl.org/rss/1.0/modules/content/"
    xmlns:wfw="http://wellformedweb.org/CommentAPI/"
    xmlns:dc="http://purl.org/dc/elements/1.1/"
    xmlns:wp="http://wordpress.org/export/1.2/"
    exclude-result-prefixes="xs"
    version="2.0">
    <xsl:template match="/">
        <root>
            <xsl:apply-templates/>
        </root>
    </xsl:template>
    <xsl:template match="item">
        <xsl:if test="count(./content:encoded) = 1">
            <xsl:element name="item">
                <xsl:element name="content">
                    <xsl:copy-of select="content:encoded/text()" />
                </xsl:element>
                <xsl:copy-of select="title" />
            </xsl:element>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>