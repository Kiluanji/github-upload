EAPI=7

PYTHON_COMPAT=( python3_{7..9} )

inherit distutils-r1

DESCRIPTION="Nganki Project's trading programme"
HOMEPAGE="https://github.com/Kiluanji/ngankitrading"
SRC_URI="https://github.com/Kiluanji/ngankitrading/blob/master/tarballs/ngankitrading-0.0.1.tar.gz"

LICENSE=""
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE=""

DEPEND=">=dev-lang/python-3.8.5"
RDEPEND="${DEPEND}"
BDEPEND=""
