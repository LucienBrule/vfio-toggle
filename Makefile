# Variables
PACKAGE_NAME = vfio_toggle
VERSION = 0.1.0
SOURCE_DIR = src
BUILD_DIR = build
DIST_DIR = dist
RPMBUILD_DIR = rpmbuild
SPEC_FILE = $(PACKAGE_NAME).spec

.PHONY: all clean install rpm test dist

all: rpm

# Create the source distribution
dist: clean
	poetry build

# Package the project as an RPM
rpm: dist
	@mkdir -p $(RPMBUILD_DIR)/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
	@cp dist/$(PACKAGE_NAME)-$(VERSION).tar.gz $(RPMBUILD_DIR)/SOURCES/
	@cp $(SPEC_FILE) $(RPMBUILD_DIR)/SPECS/
	rpmbuild --define "_topdir $(PWD)/$(RPMBUILD_DIR)" -ba $(SPEC_FILE)

# Install the RPM
install: rpm
	sudo rpm -ivh $(RPMBUILD_DIR)/RPMS/x86_64/$(PACKAGE_NAME)-$(VERSION)-1.x86_64.rpm

# Run tests
test:
	pytest tests/

# Clean up build artifacts
clean:
	@rm -rf $(BUILD_DIR) $(DIST_DIR) $(RPMBUILD_DIR) *.egg-info
	@find . -name "__pycache__" -exec rm -rf {} +
