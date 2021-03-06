export CHARM_NAME := sge-client
export CHARM_BUILD_DIR ?= ../../build

# Makefile Targets
deploy-clean-model: build
	juju destroy-model sge-sandbox -y; juju add-model sge-sandbox; juju switch sge-sandbox
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

deploy: build
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

redeploy:
	juju deploy $(CHARM_BUILD_DIR)/$(CHARM_NAME) --series xenial

build: clean
	tox -e build

clean:
	rm -rf .tox/
	rm -rf $(CHARM_BUILD_DIR)/$(CHARM_NAME)

# publish the built charm
publish: build republish

republish:
	$(eval published_url := $(shell charm push $(CHARM_BUILD_DIR)/$(CHARM_NAME) | grep url | awk {'print $$2'}))
	charm release $(published_url)

