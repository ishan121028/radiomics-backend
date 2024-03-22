import { useNavigate } from "react-router-dom";
import styled from 'styled-components';

export default function Home() {
	const navigate = useNavigate();

	const createproject = () => {
		navigate("/createproject");
	}

	return (
		<Cont>
            <Topbox>
                <Box>
                    <ExistingProjects>
                        Existing Projects
                    </ExistingProjects>
                    <div data-bs-spy="scroll" data-bs-target="#navbar-example2" data-bs-root-margin="0px 0px -40%" data-bs-smooth-scroll="true" class="scrollspy-example bg-body-tertiary p-3 rounded-2" tabindex="0" style={{width: "100%", height: "90%", overflow: "auto"}} >

                        <div class="list-group">
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Leaf segmentation
                            </a>
                            <a href="#" class="list-group-item list-group-item-action">
                                Animal segmentation
                            </a>
                        </div>
                    </div>
                </Box>
            </Topbox>
            <Bottombox>
                <Createproj onClick={createproject}>
                    Create Project
                </Createproj>
            </Bottombox>
		</Cont>
	)
}

const Cont = styled.div`
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    width: 100vw;
`;

const Topbox = styled.div`
    display: flex;
    justify-content: center;
    align-items: end;
    height: 80%;
    width: 60%;
`;

const Box = styled.div`
    height: 70%;
    width: 100%;
`;

const Bottombox = styled.div`
    display: flex;
    justify-content: center;
    align-items: center;
    height: 20%;
    width: 60%;
`;

const Createproj = styled.button.attrs({
    className: 'btn btn-primary',
    })``;

const ExistingProjects = styled.div`
    margin-left: 30px;
    font-size: 18px;
    font-weight: bold;
    height: 10%;
`