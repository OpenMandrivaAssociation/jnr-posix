Name:		jnr-posix
Version:	3.2.7
Release:	1
Summary:	Common cross-platform POSIX APIs for Java
Group:		Development/Java
License:	EPL-2.0 or GPLv2 or LGPLv2+
URL:		https://github.com/jnr/jnr-posix
Source0:	https://github.com/jnr/jnr-posix/archive/refs/tags/jnr-posix-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildRequires:	jnr-parent
BuildRequires:	jnr-constants
BuildRequires:	jnr-ffi
BuildSystem:	maven

%description
Cross-platform POSIX APIs for Java, used by jnr-unixsocket.

%prep
%setup -q -n jnr-posix-jnr-posix-%{version}
# jnr-parent forces --release 8, which hides sun.misc.Signal.
# Drop that JDK 8 toolchain and compile with the current JDK.
# bnd's wildcard import cannot read a bundle version from the ASM jars.
python - <<'PY'
import re
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
text = re.sub(r"\s*<parent>.*?</parent>", "", text, count=1, flags=re.S)
text = text.replace(
	"<artifactId>jnr-posix</artifactId>",
	"<groupId>com.github.jnr</groupId>\n  <artifactId>jnr-posix</artifactId>",
	1,
)
text = re.sub(r"\s*<extensions>.*?</extensions>", "", text, count=1, flags=re.S)
text = re.sub(
	r"\s*<plugin>\s*<artifactId>maven-javadoc-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(r"\s*<jdkToolchain>.*?</jdkToolchain>", "", text, flags=re.S)
text = text.replace(
	"<artifactId>maven-compiler-plugin</artifactId>",
	"<artifactId>maven-compiler-plugin</artifactId>\n        <version>3.12.1</version>",
	1,
)
text = text.replace(
	"<artifactId>maven-jar-plugin</artifactId>",
	"<artifactId>maven-jar-plugin</artifactId>\n        <version>3.3.0</version>",
	1,
)
text = re.sub(
	r"\s*<plugin>\s*<groupId>org\.apache\.felix</groupId>\s*<artifactId>maven-bundle-plugin</artifactId>.*?</plugin>",
	"",
	text,
	count=1,
	flags=re.S,
)
text = re.sub(r"\s*<manifestFile>.*?</manifestFile>", "", text, count=1, flags=re.S)
if "<properties>" not in text:
	text = text.replace(
		"<build>",
		"<properties>\n    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n  </properties>\n\n  <build>",
		1,
	)
path.write_text(text)
PY

%files -f .mfiles
%doc LICENSE.txt README.md
