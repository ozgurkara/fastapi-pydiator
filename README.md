# What is the purpose of this repository
This project is an example that how to implement fast-API and the pydiator-core. You can see the detail of the pydiator-core on this link https://github.com/ozgurkara/pydiator-core 

# How to run app
`uvicorn app.main:app --reload`

swagger http://0.0.0.0:8000/docs

# How to run Unit & Integration Test
`coverage run --source app/ -m pytest`

`coverage report -m`

`coverage html`


# What is the pydiator?
Pydiator is an in-app communication method. 

It provides that developing the code as an aspect. Also, it supports clean architecture infrastructure

It is using design patterns such as chain of responsibility, mediator, singleton.

Pydiator provides which advantages to developers and project?
* Is testable
* Has Use case support
* Has Aspect programming (Authorization, Validation, Cache, Logging, Tracer etc.) support
* Has Clean architecture support
* Expandable architecture via pipeline
* Is independent framework
 
![pydiator](https://raw.githubusercontent.com/ozgurkara/pydiator-core/master/assets/pydiator_flow.png)

# How it works? 
Pydiator knows 4 object types. 
These are;

**1- Request object** 
   * Is used for calling the use case.
   * It should be inherited from **BaseRequest**
   ```python 
    class GetSampleByIdRequest(BaseRequest):
        def __init__(self, id: int):
            self.id = id
   ```
<hr>

**2- Response object**
   * Is used for returning from use case
   * It should be inherited from **BaseResponse**
   ```python
   class GetSampleByIdResponse(BaseResponse):
        def __init__(self, id: int, title: str):
            self.id = id
            self.title = title 
   ``` 

<hr>

**3- Use Case**
   * Includes logic codes    
   * It should be inherited from **BaseHandler**
   * It takes one parameter to handle. The parameter should be inherited **BaseRequest** 
   ```python
   class GetSampleByIdUseCase(BaseHandler):
        async def handle(self, req: GetSampleByIdRequest):
            # related codes are here such as business
            return GetSampleByIdResponse(id=req.id, title="hello pydiator")     
   ``` 

<hr>

**What is the relation between these 3 object types?**

Every use case object only knows a request object

Every request object is only used by one use case object

<br/>

**How is the use case run?**

Should be had a particular map between the request object and the use case object.

Mapping example;
```python
    def set_up_pydiator():
        container = MediatrContainer()
        container.register_request(GetSampleByIdRequest, GetSampleByIdUseCase())
        #container.register_request(xRequest, xUseCase())
        pydiator.ready(container=container)
```

Calling example;
```python
    await pydiator.send(GetByIdRequest(id=1))
````
or
```python    
    loop = asyncio.new_event_loop()
    response: GetByIdResponse = loop.run_until_complete(pydiator.send(GetByIdRequest(id=1)))
    loop.close()
    print(response.to_json())
```

<hr>

**4- Pipeline**

The purpose of the pipeline is to manage the code as an aspect. 
For instance, you want to write a log for the request and the response of every use case. You can do it via a pipeline easily. You can see the sample log pipeline at this link.

You can create a lot of pipelines such as cache pipeline, validation pipeline, tracer pipeline, authorization pipeline etc. 

Also, you can create the pipeline much as you want but you should not forget that every use case will be used in this pipeline.

<br/>

You can add the pipeline to pipelines such as;
```python
    def set_up_pydiator():
        container = MediatrContainer()        
        container.register_pipeline(LogPipeline())
        #container.register_pipeline(xPipeline())
        pydiator.ready(container=container)
````
<br/>

***How can I write custom pipeline?***
   * Every pipeline  should be inherited ***BasePipeline***
   * Sample pipeline
```python
    class SamplePipeline(BasePipeline):
        def __init__(self):
            pass
    
        async def handle(self, req: BaseRequest) -> object:
            
            # before executed pipeline and uce case

            response = await self.next().handle(req)
    
            # after executed next pipeline and use case            

            return response
```   



