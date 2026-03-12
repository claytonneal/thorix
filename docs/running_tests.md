# Running Tests

## Unit Tests

Tests in folder `/tests/unit` don't require solo to be up, they can be executed using:

```
make test-unit
```

## Solo Tests

Most integration tests can be executed against Thor Solo, this requires Docker to be installed  
They can be executed using:


```
make solo-up
make test-solo
make solo-down
```

## Code Coverage

All tests can be executed and a combined code coverage report generated using:

```
make test
```

code coverage files created:

* coverage.xml
* .coverage
* htmlcov
