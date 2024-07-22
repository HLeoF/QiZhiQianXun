from loguru import logger
from qdrant_client import QdrantClient
from Module.configuration import QDRANT_HOST, QDRANT_PORT
from qdrant_client.http.exceptions import UnexpectedResponse
from qdrant_client.http.models import Distance, VectorParams, Batch

class VCDB:
    def __init__(self):
        self.client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT,timeout=60)
        self.size = 1536

    
    # Build a collection
    def set_collection(self, collection_name):
        """
        This is a function to build a qdrant vector collection

        Args:
            collection_name : Qdrant vector points collection name

        Returns:
            True: Qdrant vector points collection created
            False: Qdrant vector points collection failure to create
        """
        return self.client.recreate_collection(
            collection_name=collection_name, vectors_config=VectorParams(size=self.size, distance=Distance.COSINE)
        )


    # Get the info of the collection
    def get_collection(self, collection_name):
        """
        Get the specific Qdrant vector points collcetion information
        Args:
            collection_name: Qdrant Vector Points collection name 

        Returns:
            Qdrant Vector Points Collection name
        """
        collection_info = self.client.get_collection(collection_name=collection_name)
        return collection_info
    
    # Check whether a collection already exist
    def check_collection(self, collection_name):
        """
            Checking a Qdrant vector points collection whether exist
        Args:
            collection_name: Qdrant Vector points collection name

        Returns:
            Number of Vector Points in a Collection
        """
        try:
            collection_info = self.get_collection(collection_name)
        except (UnexpectedResponse, ValueError) as e:
            if self.set_collection(collection_name):
                logger.success(f"Create A Collection Successfully -> Collection Name: {collection_name} (Points Count: 0)")
                return 0
            else:
                logger.error(f"Fail to Create A Collection: {collection_name} Due to {e}")
                return -1
        except Exception as e:
            logger.error(f"Error for Obtaining Collection ({collection_name})'s Info -> {e}")
        else:
            points_count = collection_info.points_count
            logger.success(f"Collection: ({collection_name}) alrealy created -> Points Count: {points_count}")
            return points_count
    
    #Obtain Collection name list
    def collection_name_list(self):
        """
            Get list of Collection name
        Returns:
            A list of Collection name
        """
        collectionResponse = self.client.get_collections()
        collection_names_list = [collectionDescription.name for collectionDescription in collectionResponse.collections]
        return collection_names_list
    

    def add_vector_points(self, collection_name, vectors, payloads):
        """
            add vector points to a Qdrant collection
        Args:
            collection_name: The Qdrant collection name
            vectors : vector points need to upsert
            payloads: The meaning represented by vector points

        Returns:
            Bool
        """
        self.client.upsert(
            collection_name=collection_name,
            wait=True,
            points=Batch(
                ids=list(range(1, len(vectors) + 1)),
                payloads=payloads,
                vectors=vectors
            )
        )
        print("Vector Points Have been Added :)")
        return True
    
    def search(self, collection_name, query_vector, limit = 2):
        """
            Search for the most relevant vectors
        Args:
            collection_name: Qdrant collection name
            query: Query vector point
            limit: Number of result 

        Returns:
            search result
        """
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit,
            with_payload=True
        )
    

    def get_collection_content(self, collection_name, limit=1000):
        """
            Get content inside a collection
        Args:
            collection_name: Qdrant Collection name
            limit: limitation

        Returns:
            content of a collection
        """
        scored_points = self.client.search (
            collection_name=collection_name,
            query_vector=[0.0]*self.size,
            limit = limit,
            with_payload=True
        )

        #sort object by id 
        scored_points.sort(key=lambda point:point.id)
        logger.info(f"Current Collection ({collection_name}) Scored Points:{len(scored_points)}")

        page_contents = [scored_point.payload.get('page_content','') for scored_point in scored_points]
        content = "".join(page_contents)
        logger.info(f"Current Collection ({collection_name}) characters: {len(content)}")
        
        return content
    
if __name__ == "__main__":
    qdrant = VCDB()

    # 创建集合
    collection_name = "test"
    qdrant.set_collection(collection_name)
    qdrant.get_collection(collection_name)
    # 如果之前没有创建集合，则会报以下错误
    # qdrant_client.http.exceptions.UnexpectedResponse: Unexpected Response: 404 (Not Found)
    # Raw response content:
    # b'{"status":{"error":"Not found: Collection `test` doesn\'t exist!"},"time":0.000198585}'

    # 获取集合信息，如果没有该集合则创建
    # count = qdrant.get_points_count(collection_name)
    # print(count)
    # 如果之前没有创建集合，且正确创建了该集合，则输出0。例：创建集合成功。集合名：test。节点数量：0。
    # 如果之前创建了该集合，则输出该集合内部的节点数量。例：库里已有该集合。集合名：test。节点数量：0。

    # 删除集合
    # collection_name = "test"
    # qdrant.client.delete_collection(collection_name)

    # 查询集合内容
    # collection_name = ""
    # content = qdrant.get_collection_content(collection_name)
    # print(content)