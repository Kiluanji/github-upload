# REMEMBER TO DELETE ALL HASHES

EAPI=7

PYTHON_COMPAT=( python3_{7..9} ) # Which Python versions it is compatible with

inherit distutils-r1 # inherit the eclass that handles most of the python stuff

DESCRIPTION="Nganki Project's trading programme"
HOMEPAGE="https://github.com/Kiluanji/ngankitrading"
# SRC_URI lists everything that needs to be downloaded
SRC_URI="https://github.com/Kiluanji/ngankitrading/raw/master/ngankitrading-0.0.1.tar.gz"

LICENSE=""
SLOT="0"
KEYWORDS="~amd64 ~x86"
IUSE="" # This is where USE flags go

# I might need to add python dependencies here, but ask irc chat
# RDEPEND=run dependencies; BDEPEND=build dependencies
DEPEND=">=dev-lang/python-3.8.5"
RDEPEND="${DEPEND}"
BDEPEND=""


# Look to ebuild functions (in devmanual) on which functions to define, e.g. src_prepare
# check out funtoo.org as well

# I think I need a src_unpack - it extracts the source packages.
